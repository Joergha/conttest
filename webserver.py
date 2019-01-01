#!/usr/bin/env python
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
from sudoku import sudoku, print_sudoku
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

    def do_POST(self):
        # Parse query data & params to find out whit was passed
        parsedParams = urisplit(self.path)

        if parsedParams.path == '/solve':
        
            len = int(self.headers.get('Content-Length'))
            json_parsed = json.loads(self.rfile.read(len))
            s = json_parsed['s']

            print_sudoku(s)
            su = sudoku()
            if su.setSudoku(s):
                su.solve()
                print("Time Elapsed [s]: " + str(su.getElapsedTime()))
                res = '{ "s": "' + su.getResult() + '", "err": "' + su.getErrorMsg() + '", "time": "' + str(su.getElapsedTime()) + '"}'
            else:
                res = '{ "s": "' + s + '", "err": "' + su.getErrorMsg() + '", "time": "0.00"}'
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(res,"utf-8"))

Handler = MyRequestHandler
server = socketserver.TCPServer(('0.0.0.0', 80), Handler)

print("********************************************************")
print("*                 sudoku solver server                 *")
print("* HTTP-Server listening ono Port 80. Just enter the    *")
print("* Ip-Adresse in your browser                           *")
print("********************************************************")
server.serve_forever()