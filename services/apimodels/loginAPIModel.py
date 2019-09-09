from appbase import global_api
from flask_restplus import fields

loginmodel = global_api.model("Login", {
    "username": fields.String(required=True, description="用户名"),
    "password": fields.String(required=True, description="密码")
})
