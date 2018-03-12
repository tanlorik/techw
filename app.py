import json
import sys
import uuid
import base64
import hashlib
import os
import shutil
import zipfile

from cgi import parse_header, parse_multipart


if sys.version.startswith('3'):
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import urlparse, parse_qs, unquote
    _py3_ = True
else:
    from urlparse import urlparse, parse_qs, unquote
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
    _py3_ = False

##########Globals################    

_DEBUG_ = True
_FOLDER_PATHS_ = os.getcwd()
_APP_ROOT_ = "www"


#########Py3Compat###############
def make_bytes(data):

    if _py3_ :
        return bytes(data, "utf-8")
    return data    

def make_str(data):

    if _py3_:
        return data.decode("utf-8")
    return data

#########Functions###############



class S(BaseHTTPRequestHandler):
    def _set_headers(self, method):
        self.send_response(200)
        if method == "post":
            self.send_header('Content-type', 'application/json')
        else:
            self.send_header('Content-type', 'text/html')
            
        self.end_headers()

    def _set_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        

        
    def _get_args(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length), 
                    keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def _parse_path(self, path):
        
        return [x.strip() for x in path.split("/")]

    def _parse_request(self, method):
        self._set_headers(method)
        parsed_path = urlparse(self.path)
        request_id = unquote(parsed_path.path)
        path_args = self._parse_path(request_id)
        vars = self._get_args()
        fixed_vars = {}
        for item in vars:
            fixed_vars[item] = vars[item][0]
        if "report" in path_args:
            report(fixed_vars)
                

    def do_GET(self):
        parsed_path = urlparse(self.path)
        request_id = unquote(parsed_path.path)[1:]
        
        if request_id == "":
            request_id = "index.html"
        print(request_id)
        print(os.path.join(_APP_ROOT_, request_id))
        if os.path.exists(os.path.join(_APP_ROOT_, request_id)):
            self._set_headers("get")
            data = open(os.path.join(_APP_ROOT_, request_id), 'r').read()
            self.wfile.write(make_bytes((data)))
        else:
            self._set_404()

    def do_POST(self):
        self._parse_request(method="post")


    def do_HEAD(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=S, port=None):
    if port is None:
        port = int(os.environ.get('PORT'))
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        run(port=int(sys.argv[1]))
    else:
        run()