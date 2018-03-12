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


def encode_file(file_path):

    content = open(file_path, 'rb').read()
    return make_str(base64.b64encode(content))
    
    
def serve(args):

    vm_id = args[0]
    vm_os = args[1]
    
    
    
    retval = {}
    #retval["archive"] = encode_file()  -- Aici trebuie pus path-ul catre arhiva care trebuie trimisa
    
    self.wfile.write(make_bytes(json.dumps(retval)))

def log(what, timestamp, folder_path):

    with open(os.path.join(folder_path, "log.txt"), "a") as f:
        f.write("[{}] {}".format(timestamp, what))

def make_path(current, remaining):

    if "\\" in remaining:
        remaining = remaining.replace("\\", "/")
    if ":" in remaining:
        remaining = remaining.replace(":", "")
    parts = remaining.split("/", 1)
    if len(parts) == 1:
        return os.path.join(current, parts[0])
    if not os.path.exists(os.path.join(current, parts[0])):
        os.mkdir(os.path.join(current, parts[0]))
    return make_path(os.path.join(current, parts[0]), parts[1])

def make_zip(folder, file_path):

    zipf = zipfile.ZipFile(file_path+".zip", 'w', zipfile.ZIP_DEFLATED)
    ignore_path = folder + "\\"
    for root, dirs, files in os.walk(folder):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.join(root, file).replace(ignore_path, ""))
    zipf.setpassword("infected")
    zipf.close()
    
def report(args):

    job_id = make_str(args["job_id"])
    vm_id = make_str(args["vm_id"])
    type = make_str(args["type"])
    timestamp = make_str(args["timestamp"])
    action = make_str(args["action"])
    
    folder_name = "{}_{}_{}".format(vm_id, job_id, type)
    folder_path = os.path.join(_FOLDER_PATHS_, folder_name)
    
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        
    if action == "log" :
        log(make_str(args["text"]), timestamp, folder_path)
        return True

    elif action == "upload":
        path = make_str(args["path"])
        content = base64.b64decode(make_str(args["file"]))
        print(len(content))
        
        file_name = os.path.basename(path)
        
        fp = make_path(folder_path, path)
        print("fp is:", fp)
        md5 = hashlib.md5(content).hexdigest()
        with open("{}.{}".format(fp, md5), 'wb') as f:
            f.write(content)
        log("Change detected in file: {} with md5: {}\n".format(file_name, md5), timestamp, folder_path)
        return True
    elif action == "done":
        make_zip(folder_path,folder_path)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
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
        self._set_headers()
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
        self.send_response(405)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(make_bytes("<h1>This server only supports HEAD/POST requests</h1></br>"))
        if _DEBUG_:
            parsed_path = urlparse(self.path)
            request_id = unquote(parsed_path.path)
            self.wfile.write(make_bytes("path is: {}".format(request_id)))

    def do_POST(self):
        self._parse_request(method="post")


    def do_HEAD(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=S, port=None):
    if port is None:
        port = os.environ.get('PORT')
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        run(port=int(sys.argv[1]))
    else:
        run()