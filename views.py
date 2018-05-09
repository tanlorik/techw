import models
import json

_py3_ = True


#########Py3Compat###############
def make_bytes(data):

    if _py3_ :
        return bytes(data, "utf-8")
    return data    

def make_str(data):

    if _py3_:
        return data.decode("utf-8")
    return data

#################################





def get_json(wfile, args):

    wfile.write(make_bytes(json.dumps(args)))











def router(path, wfile, method, args=None):
    print(args)
    get_json(wfile, args)