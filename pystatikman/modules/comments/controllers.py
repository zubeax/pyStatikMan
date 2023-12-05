__author__ = 'Axel Zuber'

import math
from flask import Blueprint, jsonify, request
from pystatikman.utils.decorators import crossdomain
from pystatikman.modules import responses, errors, statuscodes
from pystatikman.modules.comments.models import Comment, db, CommentSchema
from sqlalchemy.exc import IntegrityError

mod = Blueprint('comments', __name__, url_prefix='/api/v<float:version>/comments')

@mod.route('/<int:comment_id>', methods=['GET'])
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
@crossdomain
def delete_comment(version, comment_id):
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
@crossdomain
def insert_comment(version):
    """
    Controller for API Function that inserts new comments in the database
    @return: Response and HTTP code
    """

    headers = request.headers
    origin = request.origin
    method = request.method
    remote_addr = request.remote_addr
    mimetype = request.mimetype
    environ = request.environ

    if mimetype.casefold() == "application/json":
        content = request.get_json(silent=True)
        # GET POST DATA
        try:
            slug = content['slug']
            parent = None
            author = content['author']
            email = content['email']
            origindomain = origin
            commenttext = content['commenttext']
        except Exception as ex:
            return jsonify(errors.error_request_incomplete(ex)), statuscodes.HTTP_NOT_ACCEPTABLE
    elif mimetype.casefold() == "application/x-www-form-urlencoded":
        formdata = request.form

        if formdata == None:
            return jsonify(errors.error_formdata_empty()), statuscodes.HTTP_NOT_ACCEPTABLE

        try:
            slug = formdata['options[slug]']
            parent = formdata['fields[parent_id]']
            author = formdata['fields[name]']
            email = author
            origindomain = origin
            commenttext = formdata['fields[message]']
        except Exception as ex:
            return jsonify(errors.error_request_incomplete(ex)), statuscodes.HTTP_NOT_ACCEPTABLE

    # API Version 1.X
    if math.floor(version) == 1:

        comment = Comment(slug, parent, author, email, origindomain, commenttext)
        db.session.add(comment)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        commentschema = CommentSchema();
        serializedcomment = commentschema.dump(comment)

        return jsonify(
            responses.create_multiple_object_response('success',
                                                      serializedcomment,
                                                      'comments')
            ), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED