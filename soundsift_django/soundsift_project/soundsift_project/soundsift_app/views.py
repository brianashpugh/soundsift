from django.shortcuts import render, render_to_response
from django.template import loader, RequestContext
from django.http import HttpResponse
import urllib2
import requests
from heapq import heappush, heappop
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

#This takes in the Souncloud username and returns a dictionary with corresponding SC information about the users'
# artists that he follows
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
    for artist_dict in artist_list:
        resultant_dictionary = {}
        try:
            artist_object = artist.Artist(artist_dict["artist_user_name"])
        except pyechonest.util.EchoNestAPIError:
            continue
        artist_name = str(artist_object)
        resultant_dictionary["artist_name"] = artist_name
        news_dict = None if len(artist_object.news) == 0 else artist_object.news[0]
        if not news_dict:
            continue
        resultant_dictionary["news_title"] = news_dict["name"]
        resultant_dictionary["news_content"] = news_dict["summary"]
        resultant_dictionary["news_url"] = news_dict["url"]
        resultant_dictionary["img_src"] = artist_dict["img_src"]
        resultant_dictionary["hotttnesss"] = artist_object.get_hotttnesss()
        resultant_list.append(resultant_dictionary)
    return resultant_list

#this takes in a list of the artist's info (including the news content/title of most recent article as well)
# and returns a list of the top LIMIT most popular artists as determined by "hotttness" level
def hotttFilter(resultant_list, limit):
    #flips the order of the prio queue so those with the highest hotttness are brought to the front
    queue = []
    for artist_dict in resultant_list:
        heappush(queue, (-artist_dict["hotttnesss"], artist_dict))
    count = 0
    most_popular_list = []
    while count < limit:
        item  = heappop(queue)
        most_popular_list.append(item)
        count += 1
    return most_popular_list


# This takes in the soundcloud user's username and returns a list of the past LIMIT artists who's tracks the user has
# liked and who is in the user's FOLLOWED_ARTISTS
def recentlyFavoritedArtists(username, followed_artists, limit):
    offset_limit = 0
    favorite_artist_counts = {}
    while True:
        favorites = client.get('users/' + username + '/favorites', offset=limit)

# Create your views here.
