from django.shortcuts import render
from django.template import loader, RequestContext
import soundcloud

client = soundcloud.Client(client_id="f504baf9fb464877d4e6d69ab6aed100")

def processUsername(request):
    def availability_query(request):
    username_dict = request.POST.dict()
    username = username_dict["sc-name-in"]
    followings = client.get('/tracks', limit=10)

# Create your views here.
