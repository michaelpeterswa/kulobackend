#!/bin/bash

gunicorn --chdir src server:app -w 2 --threads 2 -b 0.0.0.0:8888