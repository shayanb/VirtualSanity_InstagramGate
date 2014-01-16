from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from instagram import client
from models import User, Media, Auth_User
import re
import instafun

CONFIG = {
    'client_id': '77927a9402c14e37b5ae7c8904df568f',
    'client_secret': '5d2f24fb72d1489285e4013373d3cdc2',
    'redirect_uri': 'http://127.0.0.1:8000/insta/token/'    # MUST BE CHANGED in instagram developer clients too
}
scope = ["basic"]
unauthenticated_api = client.InstagramAPI(**CONFIG)


def index(request):

    return HttpResponse("Hello, world. You're at the data index. go for /gettoken")


def getoauth(request):
    try:
        url = unauthenticated_api.get_authorize_url(scope)
        response = '<a href="%s">Authenticate with Instagram</a>'
        return HttpResponse(response % url)
    except Exception, e:
        print e


def oauth(request):
    code = request.GET.get('code') #final access_token
    if not code:
        return 'Missing code'
    try:
        access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'

       # api = client.InstagramAPI(access_token=access_token)
        #recent_media, next = api.user_recent_media()
        #photos = []
        #for media in recent_media:
         #   photos.append('<img src="%s"/>' % media.images['thumbnail'].url)
          #  media2 = Media.objects.create(media_id = medias.images['media_id'], type = medias.images['type'], counts_comments = medias.images['comments']['counts'])
                         #  Media.location = medias.images['location'],

                          # Media.comments = medias['comments']['data'],

        instafun.saveAuthUser(user_info, access_token)
        instafun.saveUser(user_info, access_token)

        instafun.getUserMedia(user_info,access_token)

        return HttpResponse('All is well and all is cool')
    except Exception, e:
        print e
    #response = "the access token is %s."
    #return HttpResponse(response % code)




def user(request, user_id):
    response = "You're looking at the results of user %s."
    return HttpResponse(response % user_id)



def media(request, media_id):
    response = "You're looking at the media %s."
    return HttpResponse(response % media_id)





def tag(request, tag):
    response = "You're looking at the results of tag %s."
    return HttpResponse(response % tag)