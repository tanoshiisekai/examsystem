from appbase import global_api as api
from daos.adminloginDAO import AdminloginDAO
from flask_restplus import Resource
from flask import request
from conf import apiversion

ns_adminlogin = api.namespace("AdminLogin" + str(apiversion), description="管理员登录")

@ns_adminlogin.route("/checktoken/<string:token>")
class AdminChecktoken(Resource):

    def get(self, token):
        """
        检测token合法性
        """
        return AdminloginDAO.checktoken(token, request)


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
