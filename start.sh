#!/bin/bash

source bin/activate
exec gunicorn -c gunicorn.conf.py troebr.app:flasque

 