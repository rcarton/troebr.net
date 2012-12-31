
# -*- coding: utf-8 -*-

from jinja2 import Template, Environment, PackageLoader
import oauth2 as oauth
import private_settings
import utils
import pyblr
import time
import datetime
import urllib
import urlparse
import datetime

REQUEST_TOKEN_URL = 'http://www.tumblr.com/oauth/request_token'
AUTHORIZATION_URL = 'http://www.tumblr.com/oauth/authorize'
ACCESS_TOKEN_URL = 'http://www.tumblr.com/oauth/access_token'

DATE_FORMAT = '%Y-%m-%d %H:%M:%S GMT'

consumer = oauth.Consumer(private_settings.OAUTH_CONSUMER_KEY, private_settings.OAUTH_CONSUMER_SECRET)
client = oauth.Client(consumer)

resp, content = client.request(REQUEST_TOKEN_URL, "GET")
request_token = dict(urlparse.parse_qsl(content))
pclient = pyblr.Pyblr(client)


# post_cache
postlist_cache = dict(last_update=datetime.datetime.now(), cache=None)

def get_posts():
    """Retrieves the articles from tumblr."""
    global postlist_cache
    
    api_params = {
                  'type': 'text',
                  'limit': 5
                  }
    # 600 seconds before the cache is outdated
    if True or not postlist_cache['cache'] or (datetime.datetime.now() - postlist_cache['last_update']).seconds > 600: 
        postlist_cache['cache'] = PostList(pclient.posts(private_settings.TUMBLR_URL, api_params)['posts'])
        postlist_cache['last_update'] = datetime.datetime.now()
    
    return postlist_cache['cache']

def get_post(id):
    # No cache here for now
    return Post(pclient.posts(private_settings.TUMBLR_URL, {'id': id})['posts'][0])
    

class PostList:
    """Used as a wrapper to posts hooked to its jinja template."""
    def __init__(self, posts):
        self.posts = []
        for p in posts:
            self.posts.append(Post(p))
    
    def __str__(self):
        # Load the posts template and get this done wooo
        from app import flasque
        #flasque.jinja_env.filters['tumblr_time'] = tumblr_time_filter
        template = flasque.jinja_env.get_template('post_list.html')
        return template.render({'posts': self.posts})

class Post:
    def __init__(self, post):
        self.post = post
        self.date = datetime.datetime.strptime(self.post['date'], DATE_FORMAT)
        if post['type'] == 'text':
            self.post['page_url'] = get_slug(post)
    
    def get_formatted_date(self):
        return self.date.strftime('%Y/%m/%d')
    
    def __str__(self):
        from app import flasque
        template = flasque.jinja_env.get_template('post.html')
        return template.render({'post': self.post})

def get_slug(post):
    return utils.slugify(post['title']) + '-' + str(post['id'])

def get_id_from_slug(slug):
    return slug.split('-')[-1]

def tumblr_time_filter(s):
    return time.strftime(u'%A, %B %d, %Y', time.gmtime(time.mktime(time.strptime(s, '%Y-%m-%d %H:%M:%S %Z'))))