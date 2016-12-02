#!/usr/bin/python3
activate_file = '/var/www/{app_name}/{app_name}/venv/bin/activate_this.py'
with open(activate_file) as file_:
    exec(file_.read(), dict(__file__=activate_file))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/{app_name}/")

sys.stderr.write(sys.version)

from {app_name} import app as application
application.secret_key = '{secret_key}'

