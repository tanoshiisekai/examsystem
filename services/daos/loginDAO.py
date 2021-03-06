from appbase import global_db as gdb
from dbmodels.userDBModel import User
from sqlalchemy import and_
from tools.packtools import packinfo
from tools.auth import gettoken, getip, gettimestr, checkusertoken


class LoginDAO:

    @staticmethod
    def checkuseragent(data):
        """
        检测浏览器
        """
        if data:
            useragent = data["useragent"]
            print(useragent)
            if "mobile" in useragent:
                return packinfo(infostatus=2, infomsg="此系统不支持移动端浏览器！请切换至计算机上使用。")
            elif "firefox" in useragent:
                return packinfo(infostatus=1, infomsg="支持的浏览器")
            elif "edge" in useragent:
                return packinfo(infostatus=1, infomsg="支持的浏览器")
            elif "chrome" in useragent:
                return packinfo(infostatus=1, infomsg="支持的浏览器")
            else:
                return packinfo(infostatus=3, infomsg="此系统不支持您的浏览器！请使用Edge、Firefox或Chrome浏览器。")
        else:
            return packinfo(infostatus=-1, infomsg="系统异常！请重新打开！")



    @staticmethod
    def checktoken(username, token):
        """
        检测admin的token
        """
        if checkusertoken(username, token):
            return packinfo(infostatus=1, infomsg="合法的token")
        else:
            return packinfo(infostatus=0, infomsg="不合法的token")

    @staticmethod
    def logout(token, username, req):
        """
        用户退出
        """
        aim = gdb.session.query(User).filter(and_(
            User.user_username == username,
            User.user_token == token,
            User.user_ip == getip(req))
        ).first()
        if aim:
            # 退出系统
            aim.user_token = ""
            aim.user_ip = ""
            aim.user_logintime = ""
            try:
                gdb.session.commit()
            except Exception as e:
                print(e)
                return packinfo(infostatus=0, infomsg="数据库错误！请联系系统管理员！")
            else:
                return packinfo(infostatus=1, infomsg="成功退出系统!")
        else:
            return packinfo(infostatus=2, infomsg="异常请求！请及时修改密码！")

    @staticmethod
    def login(username, password, req):
        """
        用户登录
        """
        aim = gdb.session.query(User).filter(and_(
            User.user_username == username,
            User.user_password == password
        )).first()
        if aim:
            # 登录成功
            usertoken = gettoken()
            userip = getip(req)
            userlogintime = gettimestr()
            aim.user_token = usertoken
            aim.user_ip = userip
            aim.user_logintime = userlogintime
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
