__author__ = 'Axel Zuber'

import math
from flask import Blueprint, jsonify, request, redirect
from sqlalchemy.exc import IntegrityError

from pystatikman import app, log, log_to_file
from pystatikman.api import responses, errors, statuscodes
from pystatikman.api.comments.models import Comment, db, CommentSchema
from pystatikman.api.comments.decorators import require_origin, sanitize_request
from pystatikman.gitclient.uploader import commit_comment_to_repo
from pystatikman.utils.decorators import crossdomain

mod = Blueprint('comments', __name__, url_prefix='/api/v<float:version>/comments')

@mod.route('/<int:comment_id>', methods=['GET'])
@require_origin
@crossdomain
def get_comment(version, comment_id):
    """
    Controller for API Function that gets a comment by ID
    @param comment_id: comment id
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        comment = Comment.query.filter_by(id=comment_id).first()

        if comment is None:
            return jsonify(errors.error_object_not_found()), statuscodes.HTTP_NOT_FOUND

        commentschema = CommentSchema();
        serializedcomment = commentschema.dump(comment)

        return jsonify(
            responses.create_single_object_response('success', serializedcomment, "comment")), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/<int:comment_id>', methods=['DELETE'])
@require_origin
@crossdomain
def delete_comment(version, comment_id):
    """
    Controller for API Function that deletes a comment by ID
    @param comment_id: comment id
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        comment = Comment.query.filter_by(id=comment_id).first()

        if comment is None:
            return jsonify(errors.error_object_not_found()), statuscodes.HTTP_NOT_FOUND

        db.session.delete(comment)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        commentschema = CommentSchema();
        serializedcomment = commentschema.dump(comment)

        return jsonify(
            responses.create_single_object_response('success', serializedcomment, "comment")), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['GET'])
@require_origin
@crossdomain
def get_all_comments(version):
    """
    Controller for API Function that gets all comments in the database.
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        comments = Comment.query.all()

        commentschema = CommentSchema();

        if len(comments) == 0:
            serializedcomments = ()
        elif len(comments) == 1:
            serializedcomments = commentschema.dump(comments[0])
        else:
            serializedcomments = list(map(commentschema.dump, comments))

        return jsonify(
            responses.create_multiple_object_response('success', serializedcomments, 'comments')), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['POST', 'PUT'])
@require_origin
@sanitize_request
@crossdomain
def insert_comment(version):
    """
    Controller for API Function that inserts new comments into the database
    and commits to remote repository

    @return: Response and HTTP code
    """

#    headers = request.headers
#    environ = request.environ
#    remote_addr = request.remote_addr
    origin = request.origin
    mimetype = request.mimetype

    if mimetype == None:
        return redirect(origin, code=statuscodes.HTTP_REDIRECT)
    elif mimetype.casefold() == "application/json":
        content = request.get_json(silent=True)
        try:
            slug = content['slug']
            parent = None
            author = content['author']
            email = content['email']
            origindomain = origin
            commenttext = content['commenttext']
            blogredirectSuccess = app.config['GITHUB_PAGES_URL']+ "/comment-success.html"
            blogredirectError = app.config['GITHUB_PAGES_URL']+ "/comment-error.html"
        except Exception as ex:
            return redirect(origin, code=statuscodes.HTTP_REDIRECT)
    elif mimetype.casefold() == "application/x-www-form-urlencoded":
        formdata = request.form

        if formdata == None:
            return redirect(origin, code=statuscodes.HTTP_REDIRECT)

        try:
            slug = formdata['options[slug]']
            parent = formdata['fields[parent_id]']
            author = formdata['fields[name]']
            email = author
            origindomain = origin
            commenttext = formdata['fields[message]']
            blogredirectSuccess = formdata['options[redirect]']
            blogredirectError = formdata['options[redirectError]']
        except Exception as ex:
            return redirect(origin, code=statuscodes.HTTP_REDIRECT)
    else:
        return redirect(origin, code=statuscodes.HTTP_REDIRECT)

# API Version 1.X
    if math.floor(version) == 1:

        comment = Comment(slug, parent, author, email, origindomain, commenttext)

        try:
            db.session.add(comment)
            db.session.commit()
        except IntegrityError as ex:
            return redirect(blogredirectError, code=statuscodes.HTTP_REDIRECT)

        try:
            commit_comment_to_repo(comment)
        except Exception as ex:
            return redirect(blogredirectError, code=statuscodes.HTTP_REDIRECT)

        commentschema = CommentSchema();
        serializedcomment = commentschema.dump(comment)
        serializedcomment = str(serializedcomment)

        with log_to_file:
            log.info("Successfully processed comment: " + serializedcomment)

        return redirect(blogredirectSuccess, code=statuscodes.HTTP_REDIRECT)

    # Unsupported Versions
    else:
        return redirect(blogredirectError, code=statuscodes.HTTP_REDIRECT)
