from appbase import global_api as api
from daos.adminloginDAO import AdminloginDAO
from flask_restplus import Resource
from flask import request

ns_adminlogin = api.namespace("AdminLogin", description="管理员登录")


@ns_adminlogin.route("/<string:username>/<string:password>")
class AdminLogin(Resource):

    def get(self, username, password):
        """
        管理员登录
        """
        return AdminloginDAO.login(username, password, request)


@ns_adminlogin.route("/logout/<string:token>/<string:username>")
class AdminLogout(Resource):
    def get(self, token, username):
        """
        管理员退出
        """
        return AdminloginDAO.logout(token, username, request)
