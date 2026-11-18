#!/usr/bin/env python3
"""Local preview server: no-store so a refresh always gets the latest scene."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    ThreadingHTTPServer(('127.0.0.1', 4174), Handler).serve_forever()
