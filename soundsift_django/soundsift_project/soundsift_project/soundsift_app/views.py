from django.shortcuts import render
from django.template import loader, RequestContext
import soundcloud

client = soundcloud.Client(client_id="f504baf9fb464877d4e6d69ab6aed100")

def processUsername(request):
    def availability_query(request):
    username_dict = request.POST.dict()
    username = username_dict["sc-name-in"]
    #this includes the a list with elements as follows:
    # {artist_user_name : artist's user name,
    # description: user's description,
    # full_name: user's full_name}
    artist_list = {}
    offset_value = 0
    while True:
        followings = client.get('users/' + username + '/followings', offset=offset_value)
        if len(followings) <= 0:
            break
        for artist in followings:
            artist_list.append = {"artist_user_name": artist.username,
                                  "description": artist.description}
        offset_value += 50
    normalized_list = normalize(artist_list)
    



# Create your views here.
