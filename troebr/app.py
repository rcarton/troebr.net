#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
import time
import tumblr
from werkzeug.routing import BaseConverter

if __name__ == '__main__':
    DEBUG = True
else:
    DEBUG = False
    
SECRET_KEY = 'development key'

flasque = Flask(__name__)
flasque.config.from_object(__name__)
flasque.config.from_envvar('FLASKR_SETTINGS', silent=True)
flasque.jinja_env.filters['tumblr_time'] = tumblr.tumblr_time_filter


@flasque.route('/')
def index():
    """Landing page."""
    # TODO: Caching
    posts = tumblr.get_posts()
    return render_template('index.html', posts=posts)
    
@flasque.route('/resume')
def resume():
    return render_template('resume.html')


@flasque.route('/<slug>-<id>')
def post(slug, id):
    post = tumblr.get_post(id)
    return render_template('post_view.html', post=post)


if __name__ == '__main__':
    flasque.run('0.0.0.0',5001)

