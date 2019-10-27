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
        return ProblemsetDAO.checkexist(token, problemsetname, request)


@ns_problemset.route("/upload/<string:token>")
class ProblemSetUpload(Resource):

    @ns_problemset.expect(upload_parser)
    def post(self, token):
        """
        上传题库文件
        """
        fileobj = request.files["file"]
        return ProblemsetDAO.uploadfile(token, fileobj, request)


@ns_problemset.route("/upload/<string:token>/<string:problemtitle>/<string:problemdesp>")
class ProblemSetAdd(Resource):

    def get(self, token, problemtitle, problemdesp):
        """
        添加题库
        """
        return ProblemsetDAO.addproblemset(token, problemtitle, problemdesp, request)


@ns_problemset.route("/upload/<string:token>/<string:problemtitle>")
class ProblemSetAppend(Resource):

    def get(self, token, problemtitle):
        """
        追加题库
        """
        return ProblemsetDAO.addproblemset(token, problemtitle, "", request)


@ns_problemset.route("/<string:token>")
class ProblemSets(Resource):

    def get(self, token):
        """
        所有题库
        """
        return ProblemsetDAO.getproblemsets(token, request)


@ns_problemset.route("/remove/<string:token>/<string:problemtitle>")
class RemoveProblemSet(Resource):

    def get(self, token, problemtitle):
        """
        删除题库
        """
        return ProblemsetDAO.removeproblemsets(token, problemtitle, request)
    

@ns_problemset.route("/setting/<string:token>/<string:problemtitle>/<string:answercount>")
class AnswerCount(Resource):
    
    def get(self, token, problemtitle, answercount):
        """
        设置答题数目
        """
        return ProblemsetDAO.setanswercount(token, problemtitle, answercount, request)


@ns_problemset.route("/init/<string:token>/<string:problemtitle>")
class InitProblems(Resource):

    def get(self, token, problemtitle):
        """
        初始化答题
        """
        return ProblemsetDAO.initproblems(token, problemtitle, request)


@ns_problemset.route("/answer/<string:token>/<string:problemid>")
class GetProblem(Resource):

    def get(self, token, problemid):
        """
        获取题目
        """
        return ProblemsetDAO.getproblembyid(token, problemid, request)