import uuid
import datetime
from appbase import global_db as gdb
from dbmodels.adminDBModel import Admin
from conf import extvalid


def gettoken():
    return str(uuid.uuid4())


def getip(req):
    return req.remote_addr


def gettimestr():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def checktoken(token):
    user = gdb.session.query(Admin).filter(
        Admin.admin_token == token
    ).first()
    if user:
        return True
    else:
        return False


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in extvalid
