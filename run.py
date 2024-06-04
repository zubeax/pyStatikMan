__author__ = 'Axel Zuber'

import code
import os
import ssl
from optparse import OptionParser, OptionGroup
from pystatikman import app, db

usage = "usage: %prog [options] arg"
parser = OptionParser(usage)

group_ops = OptionGroup(parser, "Operational Options",
                        "Run a development server or a debugging shell.")

group_ops.add_option("-r", "--run",
                     help="Run API (Developement Server)",
                     action="store_true", dest="run")
group_ops.add_option("-z", "--shell",
                     help="Run shell",
                     action="store_true", dest="shell")
group_ops.add_option("-i", "--init",
                     help="Initialize the application (first use)",
                     action="store_true", dest="init")

parser.add_option_group(group_ops)

(options, args) = parser.parse_args()

if options.run is True:
    print("Starting the Development HTTP server...")

    debug = app.config['DEBUG']

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('./tls/cert.pem', './tls/privkey.pem')
    context.verify_mode = ssl.CERT_OPTIONAL
    context.load_verify_locations('./tls/truststore.pem')
    app.run(debug=debug, host="0.0.0.0", ssl_context=context)

    app.run(debug=debug, host="0.0.0.0", ssl_context=context)

    print("Stopped  the Development HTTP server.")

elif options.init is True:
    print("Creating database...")
    with app.app_context():
        db.create_all()
    print("Created database.")

elif options.shell:
    with app.app_context():
        code.interact(local={
            "app": app,
            "db": db
        })

else:
    parser.print_help()