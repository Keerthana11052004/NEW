import os
import platform
import sys # Import sys
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, render_template

# Import CMS_Pro app
from CMS_Pro_Copy.app import create_app as create_cms_app

# Import PR_CREATOR app
from PR_CREATOR.app import app as pr_creator_app

# Windows compatibility for site-packages (from CMS_Pro - Copy/run.py)
if platform.system() == "Windows":
    # Explicitly add the user site-packages path where flask_babel is installed
    user_site_packages = r'c:\users\vtgs_lap_01\appdata\local\packages\pythonsoftwarefoundation.python.3.13_qbz5n2kfra8p0\localcache\local-packages\python313\site-packages'
    if user_site_packages not in os.sys.path:
        os.sys.path.append(user_site_packages)

# Create the CMS_Pro app instance
cms_app = create_cms_app(url_prefix="")

# Create a simple Flask app for the loading page
loading_app = Flask(__name__)

@loading_app.route('/')
def loading_page():
    return render_template('loading.html')

# Configure DispatcherMiddleware
# The order matters: the most specific paths should come first.
# The root path '/' is handled by the loading_app.
application = DispatcherMiddleware(loading_app, {
    '/cms': cms_app,
    '/sap': pr_creator_app
})

if __name__ == '__main__':
    port = 5000
    host = '0.0.0.0'
    print(f"🚀 Starting combined server on http://localhost:{port}")
    print(f"🌍 CMS_Pro accessible at http://localhost:{port}/cms")
    print(f"🌍 PR_CREATOR accessible at http://localhost:{port}/sap")
    run_simple(host, port, application, use_reloader=True, use_debugger=True)
