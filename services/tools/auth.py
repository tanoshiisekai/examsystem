import uuid
import datetime
from appbase import global_db as gdb
from dbmodels.adminDBModel import Admin
from dbmodels.userDBModel import User
from conf import extvalid
import hashlib
from sqlalchemy import and_


def gettoken():
    return str(uuid.uuid4())


def getip(req):
    return req.remote_addr


def gettimestr():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def checkadmintoken(token, req):
    user = gdb.session.query(Admin).filter(and_(
        Admin.admin_token == token,
        Admin.admin_ip == getip(req))
    ).first()
    if user:
        return True
    else:
        return False


def checkalltoken(token, req):
    if checkadmintoken(token, req) or checkusertoken(token, req):
        return True
    else:
        return False
    
    
def checkusertoken(token, req):
    user = gdb.session.query(User).filter(and_(
        User.user_token == token,
        User.user_ip == getip(req))
    ).first()
    if user:
        return True
    else:
        return False


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in extvalid


def getmd5(aimstr):
    newstr = hashlib.md5(aimstr.encode("utf-8")).hexdigest()
    return newstr



