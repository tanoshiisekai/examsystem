from appbase import global_api
from flask_restplus import fields

useragentmodel = global_api.model('UserAgent', {
    'useragent': fields.String(required=True, description="useragent")
})