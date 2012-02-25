
# -*- coding: utf-8 -*-

import oauth2 as oauth
import private_settings
import pyblr
import urllib
import urlparse
from jinja2 import Template, Environment, PackageLoader
import time

REQUEST_TOKEN_URL = 'http://www.tumblr.com/oauth/request_token'
AUTHORIZATION_URL = 'http://www.tumblr.com/oauth/authorize'
ACCESS_TOKEN_URL = 'http://www.tumblr.com/oauth/access_token'


consumer = oauth.Consumer(private_settings.OAUTH_CONSUMER_KEY, private_settings.OAUTH_CONSUMER_SECRET)
client = oauth.Client(consumer)

resp, content = client.request(REQUEST_TOKEN_URL, "GET")
request_token = dict(urlparse.parse_qsl(content))
pclient = pyblr.Pyblr(client)


def get_posts():
    """Retrieves the articles from tumblr."""
    return PostList(pclient.posts(private_settings.TUMBLR_URL)['posts'])

def tumblr_time_filter(s):
    return time.strftime(u'%A, %B %d, %Y', time.gmtime(time.mktime(time.strptime(s, '%Y-%m-%d %H:%M:%S %Z'))))

class PostList:
    """Used as a wrapper to posts hooked to its jinja template."""
    def __init__(self, posts):
        self.posts = posts
    
    def __str__(self):
        # Load the posts template and get this done wooo
        from app import flasque
        flasque.jinja_env.filters['tumblr_time'] = tumblr_time_filter
        template = flasque.jinja_env.get_template('post_list.html')
        
        return template.render({'posts': self.posts})
    
