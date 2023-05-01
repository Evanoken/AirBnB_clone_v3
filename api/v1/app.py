#!/usr/bin/python3
"""
This module creates a Flask app for the RESTful API
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_app(exception):
    """call storage.close()"""
    storage.close()


@app.route('/api/v1/status')
def status():
    """Return the status of the API"""
    return jsonify({"status": "OK"})

@app.errorhandler(404)
def not_found(error):
    """ Handles 404 errors by returning a JSON-formatted 404 status code response.
    """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
