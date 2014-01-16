from django.db import models

# Create your models here.


class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    loc_id = models.IntegerField()

    def __unicode__(self):
        return "Location: %s" % self.id


class Comments(models.Model):
    comment_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
    created_at = models.CharField(max_length=50)

    def __unicode__(self):
        return "Comment: %s" % self.id



class User(models.Model):
    username = models.CharField(max_length=50)
    bio = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    profile_picture = models.URLField()
    fullname = models.CharField(max_length=100)
    counts_media = models.IntegerField()
    counts_followedby = models.IntegerField()
    counts_follows = models.IntegerField()
    user_id = models.CharField(max_length=50) # e.g 287044056
   # user_feed =
   # user_counts_likes = models.IntegerField()
   # user_counts_comments = models.IntegerField()

    def __unicode__(self):
        return "User: %s" % self.username

class Media(models.Model):
    media_id = models.CharField(max_length=50) # e.g 617040648641406679_287044056
    type = models.CharField(max_length=10) #image or video
    location = models.ForeignKey(Location, related_name='media_location', blank=True)
    counts_comments = models.IntegerField()
    comments = models.ManyToManyField(Comments, related_name='media_comments', blank=True) # as foreign key? should discuss comments more
    filter = models.CharField(max_length=20, null=True)
    createdtime = models.CharField(max_length=50)
    url = models.URLField()
    counts_likes = models.IntegerField()
    users_liked = models.ManyToManyField(User, related_name='media_users_liked', blank=True)
    url_lowres = models.URLField()
    url_thumb = models.URLField()
    url_stdres = models.URLField()
    caption = models.TextField(null=True)
    user = models.ForeignKey(User)
          #  (User, related_name='media_user')
    tags = models.CharField(max_length=500, blank=True, null=True)


    #def saveMedia(self):


    def __unicode__(self):
        return "Media: %s" % self.id

class Auth_User(models.Model):
    user_id = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    access_token = models.CharField(max_length=100)

    def __unicode__(self):
        return "AuthUser: %s" % self.username
