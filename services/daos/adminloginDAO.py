from appbase import global_db as gdb
from dbmodels.adminDBModel import Admin
from sqlalchemy import and_
from tools.packtools import packinfo
from tools.auth import gettoken, getip, gettimestr, checkadmintoken


class AdminloginDAO:

    @staticmethod
    def checktoken(token, request):
        """
        检测admin的token
        """
        if checkadmintoken(token, request):
            return packinfo(infostatus=1, infomsg="合法的token")
        else:
            return packinfo(infostatus=0, infomsg="不合法的token")

    @staticmethod
    def logout(token, username, req):
        """
        管理员退出
        """
        aim = gdb.session.query(Admin).filter(and_(
            Admin.admin_username == username,
            Admin.admin_token == token,
            Admin.admin_ip == getip(req))
        ).first()
        if aim:
            # 退出系统
            aim.admin_token = ""
            aim.admin_ip = ""
            aim.admin_logintime = ""
            try:
                gdb.session.commit()
            except Exception as e:
                print(e)
                return packinfo(infostatus=0, infomsg="数据库错误！请联系系统管理员！")
            else:
                return packinfo(infostatus=1, infomsg="成功退出系统!")
        else:
            return packinfo(infostatus=0, infomsg="异常请求！请及时修改密码！")

    @staticmethod
    def login(username, password, req):
        """
        管理员登录
        """
        aim = gdb.session.query(Admin).filter(and_(
            Admin.admin_username == username,
            Admin.admin_password == password)
        ).first()
        if aim:
            # 登录成功
            usertoken = gettoken()
            userip = getip(req)
            userlogintime = gettimestr()
            aim.admin_token = usertoken
            aim.admin_ip = userip
            aim.admin_logintime = userlogintime
            try:
                gdb.session.commit()
            except Exception as e:
                print(e)
                return packinfo(infostatus=0, infomsg="数据库错误！请联系系统管理员！")
            else:
                return packinfo(infostatus=1, infomsg="登录成功!",
                                inforesult={"usertoken": usertoken})
        else:
            return packinfo(infostatus=0, infomsg="用户名或密码错误！")
