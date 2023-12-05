# A python-based drop-in replacement for Staticman

While starting my own blog on my [journey from mainframe to public cloud](https://zubeax.github.io/) 
i ran into issues when i tried to deploy and configure [Staticman](https://staticman.net/) on Heroku.
<br/>
It is quite possible that the root cause of those problem is sitting in front of the screen, but after not making
any progress for 2 days i gave up and implemented my own version.

Like Staticman, the application exposes a simple REST API that accepts POST requests from github pages,
extracts the payload and then commits a comment file to the configured github repository. 

