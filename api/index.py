import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.middleware.proxy_fix import ProxyFix
from app import app
from models import db

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Inicializar tablas en Vercel
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating tables: {e}")
