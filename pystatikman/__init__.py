# coding=utf-8
__version__ = 1.0
version = __version__

import os
from flask import Flask, render_template
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from logbook import Logger
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

# Setup SQLAlchemy
db = SQLAlchemy(app)

# Logging
log = Logger(__name__)
log_setup = ProductionLoggingSetup(app.config['LOG_LEVEL'], app.config['LOG_DIR'] + '%s.log' % app.config['APP_NAME'])
log_to_file = log_setup.get_default_setup()

## Api routing

from pystatikman.modules.comments import mod as comments_module
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

## EOF Routes.

