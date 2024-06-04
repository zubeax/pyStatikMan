# A python-based drop-in replacement for Staticman

While starting my own blog on my [journey from mainframe to public cloud](https://blog.smooth-sailing.net/)
i ran into issues when i tried to deploy and configure [Staticman](https://staticman.net/) on Heroku.
<br/>
It is quite possible that the root cause of those problem is sitting in front of the screen, but after not making
any progress for 2 days i gave up and implemented my own version.

Like Staticman, the application exposes a simple REST API that accepts POST requests from github pages,
extracts the payload and then commits a comment file to the configured github repository.



## Installation

Clone this repository and install the required packages into a .venv environment :

```bash
python3 -m venv <venv-directory>
. <venv-directory>/activate
pip3 install -r requirements.txt
```

The 'gitpython' package depends on a locally installed git client. Install that with your package manager.
Unless you already did so, create a git config file :

```bash
$ cat > ~/.gitconfig << EOT
[user]
	name = <GITHUB_ACCOUNT>
	email = <GITHUB EMAIL>
[init]
	defaultBranch = main
[pull]
	rebase = false
EOT
```

Edit the file

    ./pystatikman/config/defaultconfig.py


| Variable                | Value                                             | Description            |
|-------------------------|---------------------------------------------------|------------------------|
| GITHUB_PAGES_URL        | "https://zubeax.github.io"                                   |             |
| GITHUB_ACCOUNT          | "zubeax"                                                     |             |
| GITHUB_BOT_ACCOUNT      | "zubeax-bot"                                                 |             |
| GITHUB_BOT_TOKENFILE    | "./token"                                                    |relative to project root|
| GITHUB_REPO_REMOTE      | "https://{username}:{token}@github.com/{account}/{pagesrepo}"|don't change !|
| GITHUB_REPO_LOCAL       | "./repo"                                                     |relative to project root |
| GITHUB_COMMENT_DIRECTORY| "_data/comments"                                             |relative to GITHUB_REPO_LOCAL |

Change the repository url for your Github Pages repository, your personal account and the bot account used to commit
comments. The bot account requires just another sign-up at Github. Once it has been provisioned, invite the bot account
from your personal account for collaboration. Done.<br/>
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

## Configuring for HTTPS

After provisioning my own domain (smooth-sailing.net) i was able to use Let's Encrypt's [Certbot CLI](https://certbot.eff.org/pages/about)
to create proper certificates. They are referred to in the keyfile/certfile parameters of the gunicorn start command further down.

## Starting as systemd service

Define a service control file

```bash
cat > /etc/systemd/system/pystatikman.service << EOT
[Unit]
Description=pyStatikMan
After=network.target

[Service]
Environment=FLASK_CONFIG=production
User=root
ExecStart=gunicorn --bind=0.0.0.0:5000 --timeout=600 --log-level=debug --ssl-version=TLSv1_2  --keyfile=./tls/privkey.pem --certfile=./tls/cert.pem pystatikman:app

WorkingDirectory=/opt/pyStatikMan/
Restart=on-failure
RestartSec=30
StartLimitIntervalSec=0

[Install]
WantedBy=multi-user.target
EOT
```

then enable and start the service :

```bash
systemctl reload-daemon
systemctl enable pystatikman
systemctl start pystatikman
```
