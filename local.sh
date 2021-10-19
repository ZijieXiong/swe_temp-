#!/bin/bash

HOST=127.0.0.1
PORT=8000
ENDPOINT=API/endpoints

# run our server locally:
PYTHONPATH=$(pwd):$PYTHONPATH
FLASK_APP=$ENDPOINT flask run --host=$HOST --port=$PORT
