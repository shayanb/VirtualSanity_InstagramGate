import bottle
from bottle import route, post, run, request
from instagram import client, subscriptions

bottle.debug(True)

CONFIG = {
    'client_id': '77927a9402c14e37b5ae7c8904df568f',
    'client_secret': '5d2f24fb72d1489285e4013373d3cdc2',
    'redirect_uri': 'http://127.0.0.1:8516/oauth_callback'
}

unauthenticated_api = client.InstagramAPI(**CONFIG)

def process_tag_update(update):
    print update

reactor = subscriptions.SubscriptionsReactor()
reactor.register_callback(subscriptions.SubscriptionType.TAG, process_tag_update)

@route('/')
def home():
    try:
        url = unauthenticated_api.get_authorize_url(scope=["likes","comments"])
        return '<a href="%s">Connect with Instagram</a>' % url
    except Exception, e:
        print e

@route('/oauth_callback')
def on_callback():
    code = request.GET.get("code")
    if not code:
        return 'Missing code'
    try:
        access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'
        
        api = client.InstagramAPI(access_token=access_token)

        userInfo = api.user_info('self')
        
        recent_media, next = api.user_recent_media()
        photos = []
        for media in recent_media:
            photos.append('<img src="%s"/>' % media.images['thumbnail'].url)
        return "<br>" + str(userInfo)
    except Exception, e:
        print e

@route('/realtime_callback')
@post('/realtime_callback')
def on_realtime_callback():
    mode = request.GET.get("hub.mode")
    challenge = request.GET.get("hub.challenge")
    verify_token = request.GET.get("hub.verify_token")
    if challenge: 
        return challenge
    else:
        x_hub_signature = request.header.get('X-Hub-Signature')
        raw_response = request.body.read()
        try:
            reactor.process(CONFIG['client_secret'], raw_response, x_hub_signature)
        except subscriptions.SubscriptionVerifyError:
            print "Signature mismatch"

run(host='localhost', port=8516, reloader=True)