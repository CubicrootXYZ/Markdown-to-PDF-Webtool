# Markdown-to-PDF-Webtool
A simple and leightweight Markdown to PDF converter

# Describtion

A simple and leightweight tool for converting Markdown syntax to a PDF. 

# Parts
## API 

The API is responsible for handling requests from the frontend. The tasks are easy, so the API also works as the backend. 

## Frontend

The frontend is a simple one-pager written in HTML and JavaScript. It sends and receives stuff to/from the API. 

## Database

The database stores the PDF files, there is a dump provided that includes a routine to auto-delete files older than 5 days.

# Installation

0. Make sure to have a MySQL-Server and Python3 running.
1. Setup a MySQL database. I strongly recommend using the provided dump, the dump provides not only the database structure, but also the auto-deletion routine. 
2. Setup the API. Therefore install all needed python librarys. The API runs with `gunicorn`, install gunicorn itself and the python library (`pip3 install gunicorn`).
3. Run the API as daemon (e.g. use systemd). You can manually run it via `bash startapi.sh` in the API-folder. 
4. Change the settings in the config.ini according to your needs. The `baseurl` should be the baseurl (url without endpoint; e.g.: http://api.domain.org or http://domain.org/api) from the API, NOT the frontend. 
5. Setup the frontend, it requires HTML and JavaScript. I recommend a Webserver like Apache. 
6. The frontend uses 127.0.0.1:8080 for calling the API, if your API is elsewhere please adapt that in the index.html file. 

