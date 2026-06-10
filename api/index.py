import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.middleware.proxy_fix import ProxyFix
from app import app

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
