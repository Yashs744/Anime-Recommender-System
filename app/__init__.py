from flask import Flask

# create a Flask instance
application = Flask(__name__)

# disable interpreting trailing slash as a new rule (i.e. /users and /users/ are same)
application.url_map.strict_slashes = False

from app import errors, routes
