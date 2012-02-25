#!/bin/bash

tail -f $(cat gunicorn.conf.py | grep -Eo "\".*?\.log.*?\"")
