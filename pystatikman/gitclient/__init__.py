__author__ = 'Axel Zuber'

import os
import re
from git import Repo
from pystatikman import app

tokenfile = app.config['GITHUB_BOT_TOKENFILE']
with open(tokenfile) as f:
    token = f.read().strip()

full_local_path = app.config['GITHUB_REPO_LOCAL']

account         = app.config['GITHUB_ACCOUNT']
username        = app.config['GITHUB_BOT_ACCOUNT']
password        = token
pagesurl        = app.config['GITHUB_PAGES_URL']
pagesrepo       = re.sub(r'https?://', '', pagesurl)
remotepattern   = app.config['GITHUB_REPO_REMOTE']
remoteurl       = remotepattern.format(username=username, token=token, account=account, pagesrepo=pagesrepo)

##
#   clone a local copy of the github pages repository.
#   TODO:   find out if we can commit with a copy the head
##
if os.path.isdir(full_local_path+"/.git"):
    repo = Repo(full_local_path)
    o = repo.remotes.origin
    o.pull()
else:
    repo = Repo.clone_from(remoteurl, full_local_path)
