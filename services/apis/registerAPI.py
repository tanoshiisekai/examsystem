from appbase import global_api as api
from daos.registerDAO import RegisterDAO
from flask_restplus import Resource

ns_register = api.namespace("Register", description="用户注册")


@ns_register.route("/<string:username>/<string:password>")
class UserRegister(Resource):

    def get(self, username, password):
        """
        用户注册
        """
        return RegisterDAO.insert(username, password)