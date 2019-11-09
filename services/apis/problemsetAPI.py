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


@ns_problemset.route("/setting1/<string:token>/<string:problemtitle>/<string:answertime>")
class AnswerTime(Resource):

    def get(self, token, problemtitle, answertime):
        """
        设置答题时间
        """
        return ProblemsetDAO.setanswertime(token, problemtitle, answertime, request)


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


@ns_problemset.route("/problemanswer/<string:token>/<string:problemid>")
class ProblemAnswer(Resource):

    def get(self, token, problemid):
        """
        获取题目带答案
        """
        return ProblemsetDAO.getproblemwithanswerbyid(token, problemid, request)


@ns_problemset.route("/problemanswer/<string:token>")
class WrongProblems(Resource):

    def get(self, token):
        """
        获取用户错题列表
        """
        return ProblemsetDAO.getwrongproblemidlist(token, request)


@ns_problemset.route("/addscore/<string:token>/<string:scoreid>/<string:right>/<string:wrong>/<string:md5str>")
class AddScore(Resource):

    def get(self, token,  scoreid, right, wrong, md5str):
        """
        更新积分
        """
        return ProblemsetDAO.addscore(token, scoreid, right, wrong, md5str, request)


@ns_problemset.route("/finishedtime/<string:token>/<string:scoreid>")
class FinishedTime(Resource):

    def get(self, token, scoreid):
        """
        记录结束时间戳
        """
        return ProblemsetDAO.addfinishedtime(token, scoreid, request)


@ns_problemset.route("/wrongproblem/<string:token>/<string:problemsetid>/<string:problemid>")
class WrongProblem(Resource):

    def get(self, token, problemsetid, problemid):
        """
        添加错题
        """
        return ProblemsetDAO.addwrongproblem(token, problemsetid, problemid, request)


@ns_problemset.route("/wrongproblem/<string:token>/<string:notebookid>")
class RemoveWrong(Resource):

    def get(self, token, notebookid):
        """
        移除错题
        """
        return ProblemsetDAO.removewrongproblem(token, notebookid, request)