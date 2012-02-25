#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
import tumblr
import time


DEBUG = True
SECRET_KEY = 'development key'

flasque = Flask(__name__)
flasque.config.from_object(__name__)
flasque.config.from_envvar('FLASKR_SETTINGS', silent=True)


@flasque.route('/')
def index():
    
    # TODO: Caching
    posts = tumblr.get_posts()
    return render_template('index.html', posts=posts)
    



if __name__ == '__main__':
    flasque.run('0.0.0.0')

