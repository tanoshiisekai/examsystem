from appbase import global_api as api
from daos.loginDAO import LoginDAO
from flask_restplus import Resource
from flask import request
from apimodels.useragentModel import useragentmodel
from conf import apiversion

ns_login = api.namespace("Login"+str(apiversion), description="用户登录")


@ns_login.route("/checkagent/")
class UserAgent(Resource):

    @ns_login.expect(useragentmodel)
    def post(self):
        """
        检测浏览器
        """
        return LoginDAO.checkuseragent(api.payload)


@ns_login.route("/checktoken/<string:username>/<string:token>")
class UserChecktoken(Resource):

    def get(self, username, token):
        """
        检测token合法性
        """
        pass


@ns_login.route("/<string:username>/<string:password>")
class UserLogin(Resource):

    def get(self, username, password):
        """
        用户登录
        """
        return LoginDAO.login(username, password, request)


@ns_login.route("/logout/<string:token>/<string:username>")
class UserLogout(Resource):

    def get(self, token, username):
        """
        用户退出
        """
        return LoginDAO.logout(token, username, request)
