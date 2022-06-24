#!/usr/bin/python3 -u

import sys
import falcon
import falcon.asgi
import uvicorn
from configobj import ConfigObj
from os.path import basename

from db import Database
from api import *

try:
    cfg_file = sys.argv[1]
except IndexError:
    print("Error: Missing config file")
    print("Usage: {} <config.ini>".format(basename(sys.argv[0])))
    sys.exit(1)

try:
    cfg = ConfigObj(infile=sys.argv[1], file_error=True, raise_errors=True)
except OSError as err:
    print(err)
    sys.exit()

async def generic_error_handler(req, resp, ex, params):
    if not isinstance(ex, falcon.HTTPError):
        traceback.print_exc()
        raise falcon.HTTPInternalServerError()
    else:
        raise ex

db = Database(cfg['pg_conn_string'])

# CORS
cors_middleware = falcon.CORSMiddleware(allow_origins=cfg['allowed_origins'])

# App
app = falcon.asgi.App(middleware=[cors_middleware])
app.req_options.strip_url_path_trailing_slash = True
#app.resp_options.media_handlers.update(extra_handlers)
app.add_error_handler(Exception, generic_error_handler)

# Resources are represented by long-lived class instances
jobs = Jobs(db)
educations = Educations(db)
users = Users(db)

# Routing
app.add_route('/jobs', jobs)
app.add_route('/educations', educations)
app.add_route('/users', users)

# server
host = cfg['host']
port = int(cfg['port'])

print("Serving on {}:{} ...".format(host, port))
uvicorn.run(app, host=host, port=port)
