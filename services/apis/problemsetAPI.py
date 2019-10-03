from appbase import global_api as api
from appbase import upload_parser
from daos.problemsetDAO import ProblemsetDAO
from flask_restplus import Resource
from flask import request

ns_problemset = api.namespace("ProblemSet", description="题库管理")


@ns_problemset.route("/<string:token>/<string:problemsetname>")
class CheckProblemSet(Resource):

    def get(self, token, problemsetname):
        """
        检查题库是否存在
        """
        return ProblemsetDAO.checkexist(token, problemsetname)


@ns_problemset.route("/upload/<string:token>")
class ProblemSetUpload(Resource):

    @ns_problemset.expect(upload_parser)
    def post(self, token):
        """
        上传题库文件
        """
        fileobj = request.files["file"]
        return ProblemsetDAO.uploadfile(token, fileobj)


@ns_problemset.route("/upload/<string:token>/<string:problemtitle>/<string:problemdesp>")
class ProblemSetAdd(Resource):

    def get(self, token, problemtitle, problemdesp):
        """
        添加题库
        """
        return ProblemsetDAO.addproblemset(token, problemtitle, problemdesp)


@ns_problemset.route("/upload/<string:token>/<string:problemtitle>")
class ProblemSetAppend(Resource):

    def get(self, token, problemtitle):
        """
        追加题库
        """
        return ProblemsetDAO.addproblemset(token, problemtitle, "")


@ns_problemset.route("/<string:token>")
class ProblemSets(Resource):

    def get(self, token):
        """
        所有题库
        """
        return ProblemsetDAO.getproblemsets(token)
