from flask import Flask

app = Flask(__name__)

from flask_backend import routes  # Import your routes