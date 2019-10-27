from appbase import global_db as gdb
from dbmodels.userDBModel import User
from sqlalchemy import and_
from tools.packtools import packinfo
from tools.auth import gettoken, getip, gettimestr, checkusertoken, allowed_file


class UserSettingsDAO:

    @staticmethod
    def changepassword(token, oldpassword, newpassword, req):
        """
        修改用户密码
        """
        if checkusertoken(token, req):
            temp = gdb.session.query(User).filter(
                User.user_password == oldpassword
            ).first()
            if temp:
                temp.user_password = newpassword
                try:
                    gdb.session.commit()
                except Exception as e:
                    print(e)
                    return packinfo(infostatus=0, infomsg="数据库错误!")
                else:
                    return packinfo(infostatus=1, infomsg="密码修改成功!")
            else:
                return packinfo(infostatus=3, infomsg="原密码错误！")
        else:
            return packinfo(infostatus=2, infomsg="没有权限!")