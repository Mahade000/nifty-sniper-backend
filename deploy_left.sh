#!/bin/bash
# Simple deployment script to launch the Flask app with Gunicorn
# Usage: ./deploy_left.sh

gunicorn --bind 0.0.0.0:8080 app:app
