from flask import jsonify
from tools.info import Info


def packinfo(infostatus, infomsg=None, inforesult=None):
    return jsonify(Info(infostatus=infostatus, infomsg=infomsg, inforesult=inforesult).tojson())


def packjoinquery(resultlist):
    tempdict = {}
    for rt in resultlist:
        tempdict.update(rt.todict())
    return tempdict
