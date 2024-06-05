__author__ = 'Axel Zuber'

import os
from git import Repo
from pystatikman import app, log, log_to_file

tokenfile = app.config['GITHUB_BOT_TOKENFILE']
with open(tokenfile) as f:
    token = f.read().strip()

full_local_path = app.config['GITHUB_REPO_LOCAL']

account         = app.config['GITHUB_ACCOUNT']
username        = app.config['GITHUB_BOT_ACCOUNT']
password        = token
pagesrepo       = app.config['GITHUB_PAGES_REPO']

remotepattern   = app.config['GITHUB_REPO_REMOTE']
remoteurl       = remotepattern.format(username=username, token=token, account=account, pagesrepo=pagesrepo)

"""
  clone a local copy of the github pages repository
  or pull the latest version if .git already exists.
"""
if os.path.isdir(full_local_path+"/.git"):
    with log_to_file:
        log.info("gitclient::init - pulling repo")

    repo = Repo(full_local_path)
    o = repo.remotes.origin
    res = o.pull()

    with log_to_file:
        log.info("gitclient::init - pulled repo : " + ''.join(map(str, res)) )

else:
    with log_to_file:
        log.info("gitclient::init - cloning repo")

    repo = Repo.clone_from(remoteurl, full_local_path)

    with log_to_file:
        log.info("gitclient::init - cloned repo ")
