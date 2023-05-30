#!/usr/bin/python3
"""
    blueprint routes
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def get_status():
    """
        Get status method
    """
    return (jsonify({"status": "OK"}))
