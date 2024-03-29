from helper import timestamp_to_datetime


class ApiModel(object):

    @classmethod
    def object_from_dictionary(cls, entry):
        # make dict keys all strings
        entry_str_dict = dict([(str(key), value) for key, value in entry.items()])
        return cls(**entry_str_dict)

    def __repr__(self):
        return unicode(self).encode('utf8')


class Image(ApiModel):

    def __init__(self, url, width, height):
        self.url = url
        self.height = height
        self.width = width

    def __unicode__(self):
        return "Image: %s" % self.url


class Media(ApiModel):

    def __init__(self, id=None, **kwargs):
        self.id = id
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def get_standard_resolution_url(self):
        return self.images['standard_resolution'].url

    def __unicode__(self):
        return "Media: %s" % self.id

    @classmethod
    def object_from_dictionary(cls, entry):
        new_media = Media(id=entry['id'])

        new_media.user = User.object_from_dictionary(entry['user'])
        new_media.images = {}
        for version, version_info in entry['images'].iteritems():
            new_media.images[version] = Image.object_from_dictionary(version_info)

        new_media.type = entry['type']

        if 'user_has_liked' in entry:
            new_media.user_has_liked = entry['user_has_liked']
        new_media.like_count = entry['likes']['count']
        new_media.likes = []
        if 'data' in entry['likes']:
            for like in entry['likes']['data']:
                new_media.likes.append(User.object_from_dictionary(like))

        new_media.comment_count = entry['comments']['count']
        new_media.comments = []
        for comment in entry['comments']['data']:
            new_media.comments.append(Comment.object_from_dictionary(comment))

        new_media.created_time = timestamp_to_datetime(entry['created_time'])
        new_media.lat, new_media.lon, new_media.loc_id = (0,0,0)
        if entry['location'] and 'id' in entry:
           # new_media.location = Location.object_from_dictionary(entry['location'])
            new_media.lat, new_media.lon, new_media.loc_id = Location_info.object_from_dictionary(entry['location'])
            #new_media.location = entry['location']
            #print new_media.lat, new_media.lon, new_media.loc_id

        new_media.caption = None
        if entry['caption']:
            new_media.caption = Comment.object_from_dictionary(entry['caption'])

        if entry['tags']:
            new_media.tags = []
            for tag in entry['tags']:
                new_media.tags.append(Tag.object_from_dictionary({'name': tag}))

        new_media.link = entry['link']

        new_media.filter = entry.get('filter')

        return new_media


class Tag(ApiModel):
    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __unicode__(self):
        return "%s" % self.name


class Comment(ApiModel):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    @classmethod
    def object_from_dictionary(cls, entry):
        user = User.object_from_dictionary(entry['from'])
        text = entry['text']
        created_at = timestamp_to_datetime(entry['created_time'])
        id = entry['id']
        return Comment(id=id, user=user, text=text, created_at=created_at)

    def __unicode__(self):
        return "%s : \"%s\"" % (str(self.user.id), self.text)


class Point(ApiModel):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        print "in Point"

    def __unicode__(self):
        return "Point: (%s, %s)" % (self.latitude, self.longitude)


class Location(ApiModel):
    def __init__(self, id, *args, **kwargs):
        self.id = id
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    @classmethod
    def object_from_dictionary(cls, entry):
        point = None
        if 'latitude' in entry:
            point = Point(entry.get('latitude'),
                          entry.get('longitude'))
        location = Location(entry.get('id', 0),
                       point=point,
                       name=entry.get('name', ''))
        return location

    def __unicode__(self):
        return "Location: %s (%s)" % (self.id, self.point)


class Location_info(ApiModel):
    def __init__(self, id, *args, **kwargs):
        self.id = id
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    @classmethod
    def object_from_dictionary(cls, entry):
        point = None
        if 'latitude' in entry:
            lat = entry.get('latitude')
            lon = entry.get('longitude')
            loc_id = entry.get('id', 0)
            return (lat,lon,loc_id)
        else:
            return (0,0,0)

    def __unicode__(self):
        return "Location: %s" % (self.id)


class User(ApiModel):

    def __init__(self, id, *args, **kwargs):
        self.id = id
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __unicode__(self):
        return "%s" % self.user.id



class User_info(ApiModel):
    counts = ''
    def __init__(self, id, *args, **kwargs):
        self.id = id
        global counts
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
            if key == 'counts':
                counts = value

    def __unicode__(self):
      #  return "(Media: %i, Followed_by: %i, Follows: %i)" % (counts['media'], counts['followed_by'], counts['follows'])
        return unicode(counts)

class Relationship(ApiModel):

    def __init__(self, incoming_status="none", outgoing_status="none", target_user_is_private=False):
        self.incoming_status = incoming_status
        self.outgoing_status = outgoing_status
        self.target_user_is_private = target_user_is_private

    def __unicode__(self):
        follows = False if self.outgoing_status == 'none' else True
        followed = False if self.incoming_status == 'none' else True

        return "Relationship: (Follows: %s, Followed by: %s)" % (follows, followed)
