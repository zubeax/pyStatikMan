__author__ = 'Axel Zuber'

import os
import time
import uuid
import yaml
from git import Repo
from pystatikman import app, log, log_to_file
from pystatikman.api.comments.models import Comment

def commit_changes(repo, commentfile, message):
    """
    perform a local git commit
    :param repo: github pages repo
    :param commentfile: added comment file
    :param message: commit message
    :return:
    """
    index = repo.index
    index.add([commentfile])
    index.commit(message)

def push_changes(repo):
    """
    push the pending commit to the remote repo
    :param repo: github pages repo
    :return:
    """
    origin = repo.remote(name="origin")
    origin.push()

def commit_comment_to_repo(comment : Comment):
    """
    Github Client for uploading a comment to a Github Pages Repository
    @param comment: a comment
    @return: n/a
    """
    slug = comment.slug

    comment_uuid = str(uuid.uuid4())
    epoch_time = str(int(time.time()))

    comment_local_path = app.config['GITHUB_REPO_LOCAL']
    comment_local_path = comment_local_path + "/" + app.config['GITHUB_COMMENT_DIRECTORY']
    comment_local_path = comment_local_path + "/" + slug

    os.makedirs(comment_local_path, mode=0o777, exist_ok=True)

    # Sanitize the path
    comment_local_path = os.path.abspath(comment_local_path)

    commentfile = comment_local_path + "/" + "entry" + epoch_time + ".yml"

    f = open(commentfile, "w")

    commentdict = {
        "_id": comment_uuid,
        "parent_id": comment.parent,
        "name": comment.author,
        "message": comment.commenttext.strip(),
        "date": epoch_time
    }

    yaml.dump(commentdict, f, allow_unicode=True)

    f.close()

    repo = Repo(os.path.abspath(app.config['GITHUB_REPO_LOCAL']))
    commit_changes(repo, commentfile, slug)
    push_changes(repo)

    with log_to_file:
        log.info("Successfully pushed comment to repo")

