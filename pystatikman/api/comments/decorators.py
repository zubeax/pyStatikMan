__author__ = 'Axel Zuber'

import os, os.path
from functools import wraps
from flask import request, abort

from pystatikman import app, log, log_to_file

def require_origin(func):
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

        origin = RequestOrigin(request,app)

        if origin.accepted():
            return func(*args, **kwargs)
        else:
            with log_to_file:
                log.warning("Unauthorized address trying to use API: " + remote_addr)
            abort(401)

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
                actual_comments = len([name for name in os.listdir(comment_local_path) if os.path.isfile(comment_local_path+"/"+name)])
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


class RequestOrigin:
    """" wrapper around origin acceptance rules"""
    origin = ""
    originexpected = ""
    remote_addr = ""

    def __init__(self, request, app ):
        self.origin = request.origin
        if self.origin != None:
            self.origin = self.origin.casefold()

        self.originexpected = app.config['GITHUB_PAGES_URL'].casefold()
        self.remote_addr = request.remote_addr

    def accepted(self):
        fromcurl   = (self.origin == 'from-home' and (self.remote_addr == '192.168.100.243') or self.remote_addr == '127.0.0.1')
        fromubuntu = (self.origin == 'http://ubuntu22.kippel.de:4000')
        fromlocalhost = (self.origin == None and self.remote_addr == '127.0.0.1')

        result = fromcurl or fromubuntu or fromlocalhost

        if not result:
            result = (self.origin == self.originexpected)

        return result
