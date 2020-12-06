from flask import request

HEADERS = {"Content-Type": "application/json"}
lighthouse = "http://localhost:8000/"


def my_url(url):
    return True if url == request.url_root else False
