import models
import json
import re
import datetime
import hashlib
import uuid

_py3_ = True

#########GLOBALS#################

HTML_ESCAPE_TABLE = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
     ">": "&gt;",
     "<": "&lt;",
}

IMGUR_REGEX = r"^(https:\/\/)?(i\.)?(imgur.com\/)?[a-zA-Z0-9]*?\.(png|jpg)$"
QUESTION_TYPES = ["text", "select", "checkbox"]

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
def escape_input(text):

    return "".join(HTML_ESCAPE_TABLE.get(c,c) for c in text)

def validate_image(path):

    return re.match(IMGUR_REGEX, path) is not None


def add_new_article(args):

    error_list = []

    name = escape_input(args["Name"])
    desc = escape_input(args["Description"])
    if validate_image(args["Image"]):
        img = args["Image"]
    else:
        error_list.append("Invalid image link!")
        return error_list
    item = models.Item.create(name=name, description=desc, image_link=img)
    item.add_date = datetime.datetime.now()
    item.save()
    i = 1
    while "q{}_name".format(i) in args:
        if args["q{}_type".format(i)] not in QUESTION_TYPES:
                i += 1
                error_list.append("Question {} has an invalid type".format(i))
                continue
        q = models.Question.create(item=item)
        q.qtype = QUESTION_TYPES.index(args["q{}_type".format(i)])
        q.name = escape_input(args["q{}_name".format(i)])
        qdata = []
        j = 1
        while "q{}data{}".format(i,j) in args:
            qdata.append(escape_input(args["q{}data{}".format(i,j)]))
            j+= 1
        q.data = json.dumps(qdata)
        q.save()
    
        i+= 1


    return error_list

def login(args):

    try:
        usr = models.User.get(models.User.name == args["user"])
    except:
        return None
    stored_pwd = usr.password
    pwd = hashlib.md5(make_bytes(args["pass"])).hexdigest()
    if stored_pwd == pwd :
        usr.sid = str(uuid.uuid4())
        usr.save()
        return usr.sid
    else:
        return None

def do_vote(args):

    z = []

    itemstart = "i{}q".format(args["item_id"])
    for answer in args:
        if answer.startswith(itemstart):
            tmp = answer.replace(itemstart, "")
            try:
                qid = int(tmp)
            except:
                if "o" in tmp:
                    qid, rid = tmp.split("o", 1)
                    try:
                        qid = int(qid)
                        rid = int(rid)
                    except:
                        z.append("Sad Life")
                        continue
                else:
                        z.append("sad life v2")
                        continue
            q = models.Question.get_by_id(qid)
            r = models.Response.create(field=q, data=escape_input(args[answer]))
            r.save()
            z.append("Added {} ".format(r.data))
    return z



def do_post(wfile, args):

    if args["sub"] == "Add":
        args["errors"] = add_new_article(args)
        wfile.write(make_bytes(json.dumps(args)))
    elif args["sub"] == "Login":
        args["rez"] = login(args)
        wfile.write(make_bytes(json.dumps(args)))
    elif args["sub"] == "Vote":
        args['err'] = do_vote(args)
        wfile.write(make_bytes(json.dumps(args)))
    else:
        wfile.write(make_bytes(json.dumps(args)))


def prepare_question(q):

    qdata = {}
    qdata["id"] = q.id
    qdata["name"] = q.name
    qdata["qtype"] = q.qtype
    qdata["data"] = q.data

    return qdata


def prepare_item(item):

    data = {}

    data["id"] = item.id
    data["name"] = item.name
    data["description"] = item.description
    data["image_link"] = item.image_link
    data["question"] = []
    questions = models.Question.select().join(models.Item).where(models.Item.id == item.id)
    for q in questions:
        data["question"].append(prepare_question(q))

    return data


def get_replies(qid):

    data = {}
    replies = models.Response.select().join(models.Question).where(models.Question.id == qid)
    for reply in replies:
        if reply.data not in data:
            data[reply.data] = 0
        data[reply.data] += 1

    return data


def get_questions(iid):

    data = {}
    questions = models.Question.select().join(models.Item).where(models.Item.id == iid)
    for q in questions:
        print(q.name)
        data[q.name] = get_replies(q.id)

    return data


def do_get(wfile, args, path):

    if path == "all":
        data = []
        items = models.Item.select().order_by(models.Item.add_date.desc())
        for item in items:
            data.append(prepare_item(item))
        wfile.write(make_bytes(json.dumps(data)))
    elif path.startswith("reply"):
        id = path.replace("reply/", "")
        try:
            id = int(id)
        except:
            data = {"error": "item does not exist"}
            wfile.write(make_bytes(json.dumps(data)))
        else:
            wfile.write(make_bytes(json.dumps(get_questions(id))))
    else:
        try:
            id = int(path)
        except:
            pass
        else:
            try:
                data = prepare_item(models.Item.get_by_id(id))
                wfile.write(make_bytes(json.dumps(data)))
            except :
                data = {"error": "item does not exist"}
                wfile.write(make_bytes(json.dumps(data)))







def router(path, wfile, method, args=None):
    print(method)
    if method == "post":
        do_post(wfile, args)
    if method == "get":
        do_get(wfile, args, path)