#!/usr/bin/env python
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler

import socketserver
from uritools import urisplit
import json

class MyRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):

        # Parse query data & params to find out whit was passed
        parsedParams = urisplit(self.path)
        if parsedParams.path == '/':
            self.path = '/index.html'
        else:
            self.path = parsedParams.path
        return SimpleHTTPRequestHandler.do_GET(self)


Handler = MyRequestHandler
server = socketserver.TCPServer(('0.0.0.0', 80), Handler)

print("********************************************************")
print("*                 sudoku solver server                 *")
print("* HTTP-Server listening ono Port 80. Just enter the    *")
print("* Ip-Adresse in your browser                           *")
print("********************************************************")
server.serve_forever()