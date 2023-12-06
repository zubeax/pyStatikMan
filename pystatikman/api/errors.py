__author__ = 'Axel Zuber'

def log_exception(sender, exception, **extra):
    sender.logger.debug('Got exception during processing: %s', exception)

def error_incorrect_version(version):
    return {"status": "error", "message": "incorrect API version "+str(version)+" used."}

def error_unsupported_mimetype(mimetype):
    return {"status": "error", "message": "unsupported mimetype "+mimetype+" used."}

def error_object_not_found():
    return {"status": "error", "message": "object not found"}

def error_formdata_empty():
    return {"status": "error", "message": "submitted form is empty"}

def error_request_incomplete(ex):
    return {"status": "error", "message": "mandatory attribute missing from request", "name": ex.args[0]}

def error_commit_error(ex):
    return {"status": "error", "message": "error when committing object to database", "exception": ex.message}

def error_gitclient_error(ex):
    return {"status": "error", "message": "error when committing object to remote repository", "exception": ex.message}