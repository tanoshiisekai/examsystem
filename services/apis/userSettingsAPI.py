from appbase import global_api as api
from daos.userSettingsDAO import UserSettingsDAO
from flask_restplus import Resource
from flask import request
from conf import apiversion

ns_usersettings = api.namespace("UserSettings"+str(apiversion), description="用户设置")


@ns_usersettings.route("/<string:token>/<string:oldpassword>/<string:newpassword>")
class UserChangePassword(Resource):

    def get(self, token, oldpassword, newpassword):
        """
        修改用户密码
        """
        return UserSettingsDAO.changepassword(token, oldpassword, newpassword, request)

