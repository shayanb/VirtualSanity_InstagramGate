__author__ = 'sbeta'


import json
from django.http import HttpResponse
from instagram import client, helper
import re
from models import User, Media, Auth_User, Location, Comments
from django.core.exceptions import MultipleObjectsReturned

# All the functions has a short description in the beginning
# the used method is that each function would return the final object that it has saved in the DB (if possible)


def saveAuthUser(user_info, access_token):
    """
    saves user info and access_token in Auth_user
    """
    try:
        auth_user = Auth_User.objects.get(user_id__exact = user_info['id'])
    except Auth_User.DoesNotExist:
        auth_user = Auth_User.objects.get_or_create(user_id = user_info['id'], username = user_info['username'], access_token = access_token)
    return auth_user


def saveUser(user_info, access_token):
    """
    saves user info in User Model
    """
    api = client.InstagramAPI(access_token = access_token)
    user_info2 = api.user_info(user_info['id']) # gets the number of media/followed_by/followings


    if 'followed_by' in str(user_info2): #check to see there is access to the variables or not
        counts = re.match("{'media': (?P<media>[0-9]+), " #parsing the output of user_info
                      "'followed_by': (?P<followed_by>[0-9]+), "
                      "'follows': (?P<follows>[0-9]+)}", str(user_info2))

        counts_media = int(counts.group("media"))
        counts_followedby = int(counts.group("followed_by"))
        counts_follows = int(counts.group("follows"))
    else:
        counts_media = 0
        counts_followedby = 0
        counts_follows = 0
    try:
        userinfo = User.objects.get(user_id = user_info['id'])
        User.objects.filter(user_id = user_info['id']).update(username = user_info['username'],
        bio = user_info['bio'],
        website = str(user_info['website']),
        profile_picture = str(user_info['profile_picture']),
        fullname = user_info['full_name'],
        counts_media = counts_media,
        counts_followedby = counts_followedby,
        counts_follows = counts_follows)
    except User.DoesNotExist:
        userinfo =  User.objects.get_or_create(
        username = user_info['username'],
        bio = user_info['bio'],
        website = str(user_info['website']),
        profile_picture = str(user_info['profile_picture']),
        fullname = user_info['full_name'],
        counts_media = counts_media,
        counts_followedby = counts_followedby,
        counts_follows = counts_follows,
        user_id = user_info['id'])
    return userinfo


#def saveComments(user_id, text):

#def saveMediaLocation(media_id, lat, lon, loc_id):


       #     users_liked = users_liked.append(saveUser(image.user, access_token)),



def saveMedia(media_page, access_token):
    """
    Saves all the media the media generator (tuple of 60 media, next_url) (e.g api.user_recent_media(user_id, as_generator=True, with_next_url=next_url)
    Also creates the user of the media if it does not exist
    """
    max_next_url = ''
    for media, next_url in media_page:
        max_next_url = next_url
        for image in media:
           # user_id = '6058746'
            user_id =  image.user.id
            try:
                user = User.objects.get(user_id = user_id)
            except User.DoesNotExist:
                api = client.InstagramAPI(access_token = access_token)
                user_info = api.user_info(user_id)
                user = saveUser(user_info, access_token)

            location = Location.objects.get_or_create(lat=float(image.lat), lon=float(image.lon), loc_id=int(image.loc_id))
            users_liked = []
            print user_id #4DEBUG
            print image.id #4DEBUG


            try:
                save_media = Media.objects.get(media_id = image.id)
            except Media.DoesNotExist:

                try: # to fix no tag issue , for no tags "none" is inserted in DB
                    tag = image.tags
                except:
                    tag = 'none'

                save_media = Media.objects.get_or_create(
                    media_id = image.id,
                    type = image.type,
                    location = location[0],
                    counts_comments = int(image.comment_count),
                    # comments = '',
                    filter = image.filter,
                    createdtime = image.created_time,
                    url = str(image.link),
                    counts_likes = int(image.like_count),
                    #    users_liked = '',
                    url_lowres = str(image.images['low_resolution'].url),
                    url_thumb = str(image.images['thumbnail'].url),
                    url_stdres = str(image.images['standard_resolution'].url),
                    #  users_in = '',
                    caption = image.caption,
                    user = user,
                    tags = tag)
    return max_next_url





def getUserMedia(user_info, access_token, next_url = '0'):
    """
    saves all the user's uploaded media
    also checks if the user has not been in the database saves the whole media
    """
    user_id = user_info['id']
    api = client.InstagramAPI(access_token = access_token)
    recent_media = api.user_recent_media(user_id, as_generator=True) #, with_next_url='https://api.instagram.com/v1/users/6058746/media/recent?access_token=6058746.77927a9.9ede917f5b1a453bb77f18ea812d64bc&count=self&max_id=544333544080183134_6058746')
    max_next_url = saveMedia(recent_media, access_token)
    while max_next_url is not None:# workaround for pagination
        recent_media = [api.user_recent_media(user_id, as_generator=True, with_next_url=max_next_url)]
        next_max = saveMedia(recent_media, access_token)
        max_next_url = next_max
        print recent_media #4DEBUG





#
#def saveMedia(media):
#
#
#
#def processImages( media, subscription_id ):
#    for image in media:
#        image_query = InstagramImage.objects.filter(remote_id=image.id)
#        if len(image_query) == 1:
#            db_image = image_query[0]
#        else:
#            db_image = InstagramImage()
#            db_image.remote_id = image.id
#            db_image.thumbnail_url = image.images['thumbnail'].url
#            db_image.full_url = image.images['standard_resolution'].url
#            db_image.user = image.user.id2
#            db_image.username = image.user.username
#            db_image.usericon = image.user.profile_picture
#            db_image.subscriber = Subscription.objects.get( remote_id= subscription_id )
#            db_image.likescount = len(image.likes)
#            db_image.created_time = image.created_time
#        db_image.caption = getattr(image.caption, "text", "")
#        db_image.all_tags = json.dumps([i.name for i in image.tags])
#        db_image.comments = json.dumps([{"user":i.user.id, "text":i.text} for i in image.comments])
#
#        if hasattr(image, "location"):
#            db_image.location = image.location.name
#            db_image.lat = image.location.point.latitude
#            db_image.lng = image.location.point.longitude
#
#        db_image.save()
#
#
