from appbase import global_db as gdb
from dbmodels.userDBModel import User
from sqlalchemy import and_
from tools.packtools import packinfo
from tools.auth import gettoken, getip, gettimestr


class RegisterDAO:

    @staticmethod
    def insert(username, password):
        """
        注册用户
        """
        if not gdb.session.query(User).filter(
            User.user_username == username
            ).first():
            ad = User(username, password, "", "", "", 0, "", 0)
            try:
                gdb.session.add(ad)
                gdb.session.commit()
            except Exception as e:
                print(e)
                return packinfo(infostatus=0, infomsg="数据库错误!")
            else:
                return packinfo(infostatus=1, infomsg="注册成功!")
        else:
            return packinfo(infostatus=2, infomsg="已存在的用户名!")



