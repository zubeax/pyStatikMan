# coding=utf-8
__version__ = 1.0

version = __version__

import os
import re
from flask import Flask, render_template, redirect, request
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from logbook import Logger

from pystatikman.api import statuscodes
from pystatikman.config import definedconfigs
from pystatikman.utils.logging import ProductionLoggingSetup

# Start the Flask awesomeness.
app = Flask(__name__)

# Should we use default config (Production) or is it overridden by a environmental variable?
config_name = os.getenv('PYSTATIKMANCONFIG',
                        'DefaultConfig')  # Return the value of the environment variable PYSTATIKMANCONFIG if it exists,
                                          # or "Default" if it doesnt’t. value defaults to None.

# Setup Config
API_CONFIG = definedconfigs[config_name]
app.config.from_object(API_CONFIG)

# Verify configuration consistency

full_local_path = os.path.abspath(app.config['GITHUB_REPO_LOCAL'])
if not os.path.isdir(full_local_path):
    raise RuntimeError("repo directory $comment_local_path not found")

# Setup SQLAlchemy
db = SQLAlchemy(app)

# Logging
log = Logger(__name__)
log_setup = ProductionLoggingSetup(app.config['LOG_LEVEL'], app.config['LOG_DIR'] + '%s.log' % app.config['APP_NAME'])
log_to_file = log_setup.get_default_setup()

## Api routing
from pystatikman.api.comments import mod as comments_module
app.register_blueprint(comments_module)

"""
General purpose routes
"""

@app.route('/', methods=['GET', 'OPTIONS'])
def api_root():
    """
    Just a route that says hello to the client if he goes to the root of the API. You can remove this if you want.
    """
    body = "This is the pyStatikMan API." \
           "\n Read the docs to understand how to integrate with your github pages blog."
    return render_template('front.html', content=body, title="pyStatikMan API", version=version)

@app.route("/version", methods=['GET', 'OPTIONS'])
def api_latest_version():
    """
    Check version of the API, protected with authorization.
    """
    return str(version)

##
#   for some reason the redirect from the controller response
#   is concatenated to our domain.
#   these 2 routes are a quick fix to force the
#   redirect back to github pages.
#   for security reasons we ignore the pages repo that comes with the request
#   and instead inject the name from our configuration.
##

@app.route('/<pagesrepo>/comment-success', methods=['GET'])
def post_success(pagesrepo):
    configuredpagesrepo = app.config['GITHUB_PAGES_REPO']

    if pagesrepo != configuredpagesrepo:
        with log_to_file:
            log.info("Pages repo from request != configured: " + pagesrepo+"/"+configuredpagesrepo)

    redirecturl = 'https://{pagesrepo}/comment-success'.format(pagesrepo=configuredpagesrepo)
    return redirect(redirecturl, code=statuscodes.HTTP_REDIRECT)

@app.route('/<pagesrepo>/comment-error', methods=['GET'])
def post_error(pagesrepo):
    configuredpagesrepo = app.config['GITHUB_PAGES_REPO']

    if pagesrepo != configuredpagesrepo:
        with log_to_file:
            log.info("Pages repo from request != configured: " + pagesrepo+"/"+configuredpagesrepo)

    redirecturl = 'https://{pagesrepo}/comment-error'.format(pagesrepo=configuredpagesrepo)
    return redirect(redirecturl, code=statuscodes.HTTP_REDIRECT)

## EOF Routes.
