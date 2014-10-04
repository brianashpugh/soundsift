from django.shortcuts import render, render_to_response
from django.template import loader, RequestContext
from django.http import HttpResponse
import urllib2
import requests
import heapq
import soundcloud
from ..settings import ECHONEST_API_KEY, ECHONEST_CONSUMER_KEY
from pyechonest import config
import os
root_directory = os.path.dirname(os.path.dirname(__file__))
config.ECHO_NEST_API_KEY = ECHONEST_API_KEY


client = soundcloud.Client(client_id="f504baf9fb464877d4e6d69ab6aed100")

def renderEntryPage(request):
    fil = open(root_directory + '/soundsift_app/web/main.html')
    return HttpResponse(fil)

def processUsername(request):
    username_dict = request.POST.dict()
    username = username_dict["sc-name-in"]
    #this includes the a list with elements as follows:
    # {artist_user_name : artist's user name,
    # description: user's description,
    # full_name: user's full_name}
    artist_list = []
    offset_value = 0
    while True:
        followings = client.get('users/' + username + '/followings', offset=offset_value)
        if len(followings) <= 0:
            break
        for artist in followings:
            description = artist.description
            if description and len(description) >= 50:
                description = artist.description[:50]
            elif description:
                description = artist.description
            else:
                description = None
            artist_list.append({"artist_user_name": artist.username,
                                  "description": description,
                                  "img_src": artist.avatar_url})
        offset_value += 50
    normalized_list = normalize(artist_list)
    news_list = echonestInfoFetch(normalized_list)


#resultant dictionary is represented as follows:
# artist_name: this artist's name,
# news_title: the news' title
# news_content: the news' content
# news_url: the news' url
# img_src: the artist's sc img
def echonestInfoFetch(artist_list):
    resultant_list = []
    resultant_dictionary = {}
    for artist in artist_list:
        artist_object = artist.Artist(artist_name)
        if not artist_object:
            continue
        artist_name = str(artist_object)
        resultant_dictionary["artist_name"] = artist_name
        news_dict = artist.news
        resultant_dictionary["news_title"] = news_dict["name"]
        resultant_dictionary["news_content"] = news_dict["summary"]
        resultant_dictionary["news_url"] = news_dict["url"]
        resultant_dictionary["img_src"] = artist["img_src"]
        resultant_dictionary["hotttnesss"] = artist_object.get_hotttnesss()
        resultant_list.append(resultant_dictionary)
    return resultant_list

def hotttFilter(resultant_list):
    #flips the order of the prio queue so those with the highest hotttness are brought to the front
    queue = PriorityQueueWithFunction(lambda x: -x[1])
    for artist_dict in resultant_list:
        queue.push(artist_dict, artist_dict["hotttnesss"])
    count = 0
    most_popular_list = []
    while count < 20:
        most_popular_list.append(queue.pop())
    return most_popular_list

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.

      Note that this PriorityQueue does not allow you to change the priority
      of an item.  However, you may insert the same item multiple times with
      different priorities.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        # entry = (priority, item)
        heapq.heappush(self.heap, entry)
        self.count += 1
    def len(self):
        return len(self.heap)
    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        #  (_, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

class PriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer

    def push(self, item):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(item))

# Create your views here.
