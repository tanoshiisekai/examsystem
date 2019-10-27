from appbase import global_db as gdb
from dbmodels.adminDBModel import Admin
from sqlalchemy import and_
from tools.packtools import packinfo
from tools.auth import gettoken, getip, gettimestr, checkadmintoken, allowed_file


class AdminSettingsDAO:

    @staticmethod
    def changepassword(token, oldpassword, newpassword, request):
        """
        修改管理员密码
        """
        if checkadmintoken(token, request):
            temp = gdb.session.query(Admin).filter(
                Admin.admin_password == oldpassword
            ).first()
            if temp:
                temp.admin_password = newpassword
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