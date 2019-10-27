from appbase import global_api as api
from daos.adminSettingsDAO import AdminSettingsDAO
from flask_restplus import Resource
from flask import request

ns_adminsettings = api.namespace("AdminSettings", description="系统设置")


@ns_adminsettings.route("/<string:token>/<string:oldpassword>/<string:newpassword>")
class AdminChangePassword(Resource):

    def get(self, token, oldpassword, newpassword):
        """
        修改管理员密码
        """
        return AdminSettingsDAO.changepassword(token, oldpassword, newpassword, request)

