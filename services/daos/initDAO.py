from appbase import global_db as gdb
from dbmodels.adminDBModel import Admin
from dbmodels.settingsDBModel import Settings


class InitDAO:

    @staticmethod
    def insertadmin(username, password):
        """
        添加管理员
        """
        if not gdb.session.query(Admin).filter(
            Admin.admin_username == username,
        ).first():
            ad = Admin(username, password, "", "", "")
            gdb.session.add(ad)
            gdb.session.commit()

    @staticmethod
    def insertsettings(key, value):
        """
        添加系统设置项
        """
        if not gdb.session.query(Settings).filter(
            Settings.settings_key == key
        ).first():
            st = Settings(key, value)
            gdb.session.add(st)
            gdb.session.commit()