# A python-based drop-in replacement for Staticman

While starting my own blog on my [journey from mainframe to public cloud](https://zubeax.github.io/)
i ran into issues when i tried to deploy and configure [Staticman](https://staticman.net/) on Heroku.
<br/>
It is quite possible that the root cause of those problem is sitting in front of the screen, but after not making
any progress for 2 days i gave up and implemented my own version.

Like Staticman, the application exposes a simple REST API that accepts POST requests from github pages,
extracts the payload and then commits a comment file to the configured github repository.


## Installation

Clone this repository and edit the following file

-   ./pystatikman/config/defaultconfig.py

    GITHUB_PAGES_URL = "https://zubeax.github.io"
    GITHUB_ACCOUNT = "zubeax"
    GITHUB_BOT_ACCOUNT = "zubeax-bot"
    GITHUB_BOT_TOKENFILE  = "./token"
    GITHUB_REPO_REMOTE = "https://{username}:{token}@github.com/{account}/{pagesrepo}"
    GITHUB_REPO_LOCAL = "./repo"
    GITHUB_COMMENT_DIRECTORY  = "_data/comments"    # this is appended to GITHUB_REPO_LOCAL

Change the repository url for your Github Pages repository, your personal account and the bot account used to commit
comments. The bot account requires just another sign-up at Github. Once it has been provisioned, invite the bot account
from your personal account for collaboration. Done.
Using a bot account prevents any malfunction in pyStatikMan from messing with any of your other repos.

Generate an access token for the bot account (Settings/Developer Settings/Personal Access Token/Tokens (classic)).
Hit the 'Generate new token (classic)' button and select the 'repo' and 'user' scopes for the token.
Copy/Paste the token into the file configured as GITHUB_BOT_TOKENFILE.


## Starting the Development Server

Initialize the database with

```bash
python3 ./run.py --init
```

then start the server with

```bash
python3 ./run.py --run
```


## Starting the Production Server

Initialize the database with

```bash
python3 ./run.py --init
```

then start the server with

```bash
cd pyStatikMan
gunicorn --bind=0.0.0.0 --timeout 600 --log-level debug pystatikman:app
```
