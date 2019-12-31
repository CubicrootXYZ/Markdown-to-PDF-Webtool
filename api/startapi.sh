#!/usr/bin/env bash
#cd /mnt/d/github_repos/mdwntopdf/api
gunicorn --workers 4 -b 0.0.0.0:8080 run_old:api --reload