# src/page_tracker/app.py
"""This is a simple Flask application that
tracks the number of times a page
has been viewed using Redis."""
import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    """This is the main page of the application.
    It increments the page view count in Redis and returns the count."""
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")
        return "Sorry, something went wrong \N{PENSIVE FACE}", 500
    return f"This page has been seen {page_views} times."


@cache
def redis():
    """This function creates a Redis client.
    It uses the REDIS_URL environment variable
    to connect to the Redis server."""
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
