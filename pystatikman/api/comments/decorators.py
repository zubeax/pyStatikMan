__author__ = 'Axel Zuber'

import os, os.path
from functools import wraps
from flask import request, abort

from pystatikman import app, log, log_to_file

def require_origin(func, allow_localhost=None):
    """
    @param func: flask function
    @return: decorator, return the wrapped function or abort json object.
    """

    ##
    #   TODO:   find out how to pass parameters to the decorator function.
    #           this currently aborts with :
    #           AssertionError: View function mapping is overwriting an existing endpoint function:
    #
    #           Already tried :
    #           - wrapping the 'wrapper' function in a 'decorator' function
    #           - renaming the wrapper function
    ##

    @wraps(func)
    def wrapper(*args, **kwargs):

        origin = request.origin
        if origin != None:
            origin = origin.casefold()

        originexpected = app.config['GITHUB_PAGES_URL'].casefold()
        remote_addr = request.remote_addr

        fromcurl   = (origin == 'from-home' and (remote_addr == '84.166.222.154' or remote_addr == '192.168.100.243'))
        fromubuntu = (origin == 'http://ubuntu22.kippel.de:4000')
        fromlocalhost = (origin == None and allow_localhost and remote_addr == '127.0.0.1')
        if fromcurl or fromubuntu or fromlocalhost:
            return func(*args, **kwargs)

        if origin == None or origin != originexpected:
            with log_to_file:
                log.warning("Unauthorized address trying to use API: " + remote_addr)
            abort(401)
        else:
            return func(*args, **kwargs)

    return wrapper


def sanitize_request(func):
    """
    @param func: flask function
    @return: decorator, return the wrapped function or abort json object.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        maxblogsize = app.config['POST_MAX_SIZE']
        maxcomments = app.config['POST_MAX_COMMENTS']
        mimetype = request.mimetype

        formdata = None
        if mimetype != None and mimetype.casefold() == "application/x-www-form-urlencoded":
            formdata = request.form

        commenttext = None
        slug = None
        if formdata != None:
            try:
                commenttext = formdata['fields[message]']
                slug = formdata['options[slug]']
            except Exception as ex:
                pass

        # Prevent excessive numbers of comments

        if slug != None:
            comment_local_path = app.config['GITHUB_REPO_LOCAL']
            comment_local_path = comment_local_path + "/" + app.config['GITHUB_COMMENT_DIRECTORY']
            comment_local_path = comment_local_path + "/" + slug

            if os.path.isdir(comment_local_path):
                actual_comments = len([name for name in os.listdir(comment_local_path) if os.path.isfile(name)])
                if actual_comments > maxcomments:
                    with log_to_file:
                        log.warning("Max number of comments exceeded: " + slug)
                    abort(401)


        # Prevent excessively large comments

        if commenttext != None:
            if len(commenttext) > maxblogsize:
                with log_to_file:
                    log.warning("Max blog size exceeded: " + str(len(maxblogsize)))
                abort(401)

        return func(*args, **kwargs)

    return wrapper
