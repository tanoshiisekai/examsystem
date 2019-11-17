from appbase import global_db as gdb
from dbmodels.problemsetDBModel import ProblemSet
from dbmodels.userDBModel import User
from dbmodels.scoreDBModel import Score
from dbmodels.problemDBModel import Problem
from dbmodels.notebookDBModel import NoteBook
from sqlalchemy import and_
from tools.packtools import packinfo
from tools.auth import gettimespan, getmd5, gettoken, getip, gettimestr, checkusertoken, checkalltoken, checkadmintoken, allowed_file
import conf
import os
import zipfile
from pyexcel_xlsx import get_data as get_data_xlsx
import shutil
import os.path
import random
from flask import url_for
from sqlalchemy import func


class ProblemsetDAO:

    @staticmethod
    def copyproblemset(token, psettitle, newsettitle, req):
        """
        复制题库，可用于组织考试时清空积分
        """
        if checkalltoken(token, req):
            pset = gdb.session.query(ProblemSet).filter(
                ProblemSet.problemset_title == psettitle
            ).first()
            if pset:
                npset = ProblemSet(newsettitle, pset.problemset_desp, pset.problemset_count, pset.problemset_token,
                                   pset.problemset_answercount, pset.problemset_timeperproblem)
                try:
                    gdb.session.add(npset)
                    gdb.session.commit()
                except Exception as e:
                    return packinfo(infostatus=4, infomsg="数据库错误!")
                else:
                    newid = gdb.session.query(ProblemSet).filter(
                        ProblemSet.problemset_title == newsettitle
                    ).first().problemset_id
                    plist = gdb.session.query(Problem).filter(
                        Problem.problemset_id == pset.problemset_id
                    ).all()
                    for p in plist:
                        np = Problem(newid, p.problem_desp, p.problem_picpath, p.problem_choiceA, p.problem_choiceB,
                                     p.problem_choiceC, p.problem_choiceD, p.problem_answer)
                        gdb.session.add(np)
                    try:
                        gdb.session.commit()
                    except Exception as e:
                        return packinfo(infostatus=5, infomsg="数据库错误!")
                    else:
                        return packinfo(infostatus=1, infomsg="复制成功!")
            else:
                return packinfo(infostatus=3, infomsg="没有此题库!")
        else:
            return packinfo(infostatus=2, infomsg="没有权限!")

    @staticmethod
    def getscoresbyuseridandpsetid(userid, psetid):
        """
        通过用户编号和题库编号查询用户积分
        """
        scores = gdb.session.query(Score).filter(and_(
            Score.user_id == userid,
            Score.problemset_id == psetid
        )).all()
        if len(scores) > 0:
            scores.sort(key=lambda x: x.score_id, reverse=True)
            aim = {}
            for sc in scores:
                if len(sc.score_timestart) > 0 and len(sc.score_timeend) > 0:
                    if sc.score_right + sc.score_wrong == sc.score_problemcount:
                        if gettimespan(sc.score_timeend, sc.score_timestart) / sc.score_problemcount <= sc.problemset_timeperproblem + 3:
                            aim = sc.todict()
                            break
            aim["score_timespan"] = gettimespan(
                aim["score_timeend"], aim["score_timestart"])
            aim["problemset_title"] = gdb.session.query(ProblemSet).filter(
                ProblemSet.problemset_id == aim["problemset_id"]).first().problemset_title
            aim["user_name"] = gdb.session.query(User).filter(
                User.user_id == aim["user_id"]).first().user_username
            return aim
        return {}

    @staticmethod
    def getpsetlistbyuserid(userid):
        """
        查询用户做过的题库编号列表
        """
        psetlist = gdb.session.query(Score.problemset_id).filter(
            Score.user_id == userid
        ).distinct().all()
        return [x[0] for x in psetlist]

    @staticmethod
    def getuserlistbypsetid(psetid):
        """
        查询做某题库的用户编号列表
        """
        ulist = gdb.session.query(Score.user_id).filter(
            Score.problemset_id == psetid
        ).distinct().all()
        return [x[0] for x in ulist]

    @staticmethod
    def getscorelistbypsetid(psetid):
        """
        查询做某题库的用户成绩排名
        """
        ulist = ProblemsetDAO.getuserlistbypsetid(psetid)
        scorelist = []
        for uid in ulist:
            scorelist.append(
                ProblemsetDAO.getscoresbyuseridandpsetid(uid, psetid))
        scorelist.sort(key=lambda x: (x["score_right"]/x["score_problemcount"], 1/(
            x["score_timespan"]/x["score_problemcount"])), reverse=True)
        totaluser = len(scorelist)
        for i in range(0, len(scorelist)):
            scorelist[i]["score_rank"] = str(i + 1)+"/"+str(totaluser)
        return scorelist

    @staticmethod
    def getpsetidbypsetname(token, psetname, req):
        """
        根据题库名称，查题库编号
        """
        if checkalltoken(token, req):
            pset = gdb.session.query(ProblemSet).filter(
                ProblemSet.problemset_title == psetname
            ).first()
            if pset:
                return packinfo(infostatus=1, infomsg="查询成功!", inforesult=pset.problemset_id)
            else:
                return packinfo(infostatus=3, infomsg="没有此题库!")
        else:
            return packinfo(infostatus=2, infomsg="没有权限!")

    @staticmethod
    def getranklistbypsetid(token, psetid, req):
        """
        根据题库编号，查询排名
        """
        if checkalltoken(token, req):
            scorelist = ProblemsetDAO.getscorelistbypsetid(psetid)
            return packinfo(infostatus=1, infomsg="查询成功!", inforesult=scorelist)
        else:
            return packinfo(infostatus=2, infomsg="没有权限!")

    @staticmethod
    def getrankbypsetidanduserid(psetid, userid):
        """
        根据题库编号和用户编号获取排名
        """
        scorelist = ProblemsetDAO.getscorelistbypsetid(psetid)
        for sc in scorelist:
            if sc["user_id"] == userid:
                return sc["score_rank"]

    @staticmethod
    def getscores(token, req):
        """
        获取用户积分榜
        """
        if checkusertoken(token, req):
            us = gdb.session.query(User).filter(
                User.user_token == token
            ).first()
            usid = us.user_id
            psetlist = ProblemsetDAO.getpsetlistbyuserid(usid)
            resultlist = []
            for pid in psetlist:
                scores = ProblemsetDAO.getscorelistbypsetid(pid)
                uaim = [x for x in scores if x["user_id"] == usid]
                resultlist.append(uaim[0])
            return packinfo(infostatus=1, infomsg="查询成功!", inforesult=resultlist)
        else:
            return packinfo(infostatus=2, infomsg="没有权限!")

    @staticmethod
    def removewrongproblem(token, notebookid, req):
        """
        移除错题
        """
        if checkusertoken(token, req):
            temp = gdb.session.query(NoteBook).filter(
                NoteBook.notebook_id == notebookid
            ).first()
            if temp:
                gdb.session.delete(temp)
                try:
                    gdb.session.commit()
                except Exception as e:
                    print(e)
                    return packinfo(infostatus=0, infomsg="数据库错误!")
                else:
                    return packinfo(infostatus=1, infomsg="移除成功!")
            else:
                return packinfo(infostatus=2, infomsg="题目不存在!")
        else:
            return packinfo(infostatus=3, infomsg="没有权限!")

    @staticmethod
    def addwrongproblem(token, problemsetid, problemid, req):
        """
        添加错题
        """
        if checkusertoken(token, req):
            us = gdb.session.query(User).filter(
                User.user_token == token
            ).first()
            temp = gdb.session.query(NoteBook).filter(and_(
                NoteBook.problem_id == problemid,
                NoteBook.user_id == us.user_id
            )).first()
            if not temp:
                usid = us.user_id
                nb = NoteBook(usid, problemsetid, problemid)
                gdb.session.add(nb)
                try:
                    gdb.session.commit()
                except Exception as e:
                    print(e)
                    return packinfo(infostatus=0, infomsg="数据库错误!")
                else:
                    return packinfo(infostatus=1, infomsg="成功添加错题!")
            else:
                return packinfo(infostatus=2, infomsg="已添加的题目!")
        else:
            return packinfo(infostatus=3, infomsg="没有权限!")

    @staticmethod
    def addfinishedtime(token, scoreid, req):
        """
        记录结束时间戳
        """
        if checkusertoken(token, req):
            temp = gdb.session.query(Score).filter(
                Score.score_id == scoreid).first()
            temp.score_timeend = gettimestr()
            try:
                gdb.session.commit()
            except Exception as e:
                print(e)
                return packinfo(infostatus=0, infomsg="数据库错误!")
            else:
                return packinfo(infostatus=1, infomsg="时间更新成功!")
        else:
            return packinfo(infostatus=2, infomsg="没有权限!")

    @staticmethod
    def addscore(token, scoreid, right, wrong, md5str, req):
        """
        记录成绩
        """
        if checkusertoken(token, req):
            mstr = getmd5(getmd5(token + right + wrong) + scoreid)
            print(mstr)
            if mstr == md5str:
                if right == "1" and wrong == "0":
                    temp = gdb.session.query(Score).filter(
                        Score.score_id == scoreid).first()
                    temp.score_right = temp.score_right + 1
                    try:
                        gdb.session.commit()
                    except Exception as e:
                        print(e)
                        return packinfo(infostatus=4, infomsg="数据库错误!")
                elif right == "0" and wrong == "1":
                    temp = gdb.session.query(Score).filter(
                        Score.score_id == scoreid).first()
                    temp.score_wrong = temp.score_wrong + 1
                    try:
                        gdb.session.commit()
                    except Exception as e:
                        print(e)
                        return packinfo(infostatus=5, infomsg="数据库错误!")
                else:
                    return packinfo(infostatus=3, infomsg="请求异常！请重新登录答题!")
                return packinfo(infostatus=1, infomsg="成绩已更新！")
            else:
                return packinfo(infostatus=0, infomsg="请求异常！请重新登录答题!")
        else:
            return packinfo(infostatus=2, infomsg="没有权限！")

    @staticmethod
    def getsummarylist(token, summary_psetname, summary_pwrongpercent, req):
        """
        获取易错题列表
        """
        if checkadmintoken(token, req):
            print(token)
            print(summary_psetname)
            print(summary_pwrongpercent)
            # 查询的同时返回计数
            summarylist = gdb.session.query(NoteBook.problem_id, func.count(NoteBook.problem_id)).filter(
                NoteBook.problemset_id == gdb.session.query(ProblemSet).filter(
                    ProblemSet.problemset_title == summary_psetname).first().problemset_id
            ).group_by(NoteBook.problem_id).all()
            summarylist = [x for x in summarylist if x[1] >= int(summary_pwrongpercent)]
            summarylist.sort(key=lambda x:x[1], reverse=True)
            summarylist = [{"problem_id": x[0], "problem_count": x[1]} for x in summarylist]
            return packinfo(infostatus=1, inforesult=summarylist, infomsg="查询成功！")
        else:
            return packinfo(infostatus=2, infomsg="没有权限！")

    @staticmethod
    def getwrongproblemidlist(token, req):
        """
        获取用户错题列表
        """
        if checkusertoken(token, req):
            us = gdb.session.query(User).filter(
                User.user_token == token
            ).first()
            if us:
                usid = us.user_id
                wronglist = gdb.session.query(NoteBook).filter(
                    NoteBook.user_id == usid
                ).all()
                widlist = [{"notebookid": x.notebook_id,
                            "problemid": x.problem_id} for x in wronglist]
                # 检查作弊
                temp = gdb.session.query(Score).filter(
                    Score.user_id == usid).order_by(Score.score_id.desc()).first()
                if temp.score_timeend.strip() == "":
                    return packinfo(infostatus=-1, infomsg="正在答题", inforesult=temp.score_id)
                return packinfo(infostatus=1, inforesult=widlist, infomsg="查询成功！")
            else:
                return packinfo(infostatus=0, infomsg="用户不存在！")
        else:
            return packinfo(infostatus=2, infomsg="没有权限！")

    @staticmethod
    def getsummarywithanswerbyid(token, problemid, req):
        """
        获取易错题带答案
        """
        if checkalltoken(token, req):
            print(problemid)
            temp = gdb.session.query(Problem).filter(
                Problem.problem_id == problemid
            ).first()
            if temp:
                tempdict = temp.todict()
                answers = list(tempdict["problem_answer"])
                answers.sort()
                answers = "".join(answers)
                tempdict["problem_answer"] = answers
                return packinfo(infostatus=1, inforesult=tempdict)
            else:
                return packinfo(infostatus=0, infomsg="没有该题目！")
        else:
            return packinfo(infostatus=2, infomsg="没有权限！")

    @staticmethod
    def getproblemwithanswerbyid(token, problemid, req):
        """
        获取题目带答案
        """
        if checkalltoken(token, req):
            print(problemid)
            temp = gdb.session.query(Problem).filter(
                Problem.problem_id == problemid
            ).first()
            us = gdb.session.query(User).filter(
                User.user_token == token
            ).first()
            if temp:
                tempdict = temp.todict()
                answers = list(tempdict["problem_answer"])
                answers.sort()
                answers = "".join(answers)
                tempdict["problem_answer"] = answers
                tempscore = gdb.session.query(Score).filter(
                    Score.user_id == us.user_id).order_by(Score.score_id.desc()).first()
                if len(tempscore.score_timeend.strip()) == 0:
                    return packinfo(infostatus=-1, infomsg="答题中，无法查看错题!")
                return packinfo(infostatus=1, inforesult=tempdict)
            else:
                return packinfo(infostatus=0, infomsg="没有该题目！")
        else:
            return packinfo(infostatus=2, infomsg="没有权限！")

    @staticmethod
    def getproblembyid(token, problemid, req):
        """
        获取题目
        """
        if checkusertoken(token, req):
            print(problemid)
            temp = gdb.session.query(Problem).filter(
                Problem.problem_id == problemid
            ).first()
            tempset = gdb.session.query(ProblemSet).filter(
                ProblemSet.problemset_id == temp.problemset_id
            ).first()
            tempuser = gdb.session.query(User).filter(
                User.user_token == token
            ).first()
            tempscore = gdb.session.query(Score).filter(
                Score.user_id == tempuser.user_id).order_by(Score.score_id.desc()).first()
            if len(tempscore.score_timeend.strip()) != 0:
                return packinfo(infostatus=-1, infomsg="答题被终止!")
            if temp:
                tempdict = temp.todict()
                answers = list(tempdict["problem_answer"])
                answers.sort()
                answers = "".join(answers)
                print(answers)
                tempdict["problem_answer"] = getmd5(getmd5(str(answers) +
                                                           str(tempdict["problem_id"]))+str(answers))
                tempdict["problemset_timeperproblem"] = tempset.problemset_timeperproblem
                problemseat = tempuser.user_problemseat
                problemstream = tempuser.user_problemstream
                print("pseat:", problemseat)
                print("pstream:", problemstream)
                streamlist = problemstream.split("#")
                if streamlist.index(str(problemseat)) < len(streamlist) - 1:
                    nextpid = streamlist[streamlist.index(
                        str(problemseat)) + 1]
                    tempuser.user_problemseat = nextpid
                    try:
                        gdb.session.commit()
                    except Exception as e:
                        print(e)
                        return packinfo(infostatus=3, infomsg="数据库错误！")
                else:
                    nextpid = -1
                tempdict["problem_nextpid"] = nextpid
                return packinfo(infostatus=1, inforesult=tempdict)
            else:
                return packinfo(infostatus=0, infomsg="没有该题目！")
        else:
            return packinfo(infostatus=2, infomsg="没有权限！")

    @staticmethod
    def initproblems(token, problemtitle, req):
        """
        初始化答题
        """
        if checkusertoken(token, req):
            temp = gdb.session.query(ProblemSet, Problem).filter(and_(
                ProblemSet.problemset_title == problemtitle,
                Problem.problemset_id == ProblemSet.problemset_id
            )).all()
            if temp:
                problemids = [x[1].problem_id for x in temp]
                problemanswercount = temp[0][0].problemset_answercount
                problemsetid = temp[0][0].problemset_id
                random.shuffle(problemids)
                aimproblems = problemids[:problemanswercount]
                aimproblems = [str(x) for x in aimproblems]
                userproblemstream = "#".join(aimproblems)
                userproblemsetid = problemsetid
                userproblemseat = problemids[0]
                firstpid = userproblemseat
                user = gdb.session.query(User).filter(
                    User.user_token == token
                ).first()
                if user:
                    user.user_problemsetid = userproblemsetid
                    user.user_problemstream = userproblemstream
                    user.user_problemseat = userproblemseat
                    try:
                        gdb.session.commit()
                        timestart = gettimestr()
                        sco = Score(user.user_id, problemsetid, 0, 0,
                                    timestart, "", temp[0][0].problemset_answercount, temp[0][0].problemset_timeperproblem)
                        gdb.session.add(sco)
                        try:
                            gdb.session.commit()
                        except Exception as e:
                            print(e)
                            return packinfo(infostatus=0, infomsg="数据库错误!")
                        else:
                            scoretemp = gdb.session.query(Score).filter(and_(
                                Score.user_id == user.user_id,
                                Score.score_timestart == timestart
                            )).first()
                            scoreid = scoretemp.score_id
                    except Exception as e:
                        print(e)
                        return packinfo(infostatus=0, infomsg="数据库错误!")
                    else:
                        return packinfo(infostatus=1, infomsg="初始化答题成功!",
                                        inforesult=[firstpid, scoreid])
                else:
                    return packinfo(infostatus=2, infomsg="用户不存在!")
            else:
                return packinfo(infostatus=3, infomsg="没有该题库!")
        else:
            return packinfo(infostatus=4, infomsg="没有权限!")

    @staticmethod
    def setanswercount(token, problemtitle, answercount, req):
        """
        设置答题数目
        """
        if checkadmintoken(token, req):
            temp = gdb.session.query(ProblemSet).filter(
                ProblemSet.problemset_title == problemtitle
            ).first()
            if temp:
                temp.problemset_answercount = answercount
                try:
                    gdb.session.commit()
                except Exception as e:
                    print(e)
                    return packinfo(infostatus=0, infomsg="数据库错误!")
                else:
                    return packinfo(infostatus=1, infomsg="答题数目更新成功!")
            else:
                return packinfo(infostatus=3, infomsg="不存在的题库!")
        else:
            return packinfo(infostatus=2, infomsg="没有权限!")

    @staticmethod
    def setanswertime(token, problemtitle, answertime, req):
        """
        设置答题时间
        """
        if checkadmintoken(token, req):
            temp = gdb.session.query(ProblemSet).filter(
                ProblemSet.problemset_title == problemtitle
            ).first()
            if temp:
                temp.problemset_timeperproblem = answertime
                try:
                    gdb.session.commit()
                except Exception as e:
                    print(e)
                    return packinfo(infostatus=0, infomsg="数据库错误!")
                else:
                    return packinfo(infostatus=1, infomsg="答题时间更新成功!")
            else:
                return packinfo(infostatus=3, infomsg="不存在的题库!")
        else:
            return packinfo(infostatus=2, infomsg="没有权限!")

    @staticmethod
    def removeproblemsets(token, problemsetname, req):
        """
        移除题库
        """
        if checkadmintoken(token, req):
            temp = gdb.session.query(ProblemSet).filter(
                ProblemSet.problemset_title == problemsetname
            ).first()
            if temp:
                pid = temp.problemset_id
                probs = gdb.session.query(Problem).filter(
                    Problem.problemset_id == pid
                ).all()
                for pb in probs:
                    gdb.session.delete(pb)
                gdb.session.delete(temp)
                try:
                    gdb.session.commit()
                except Exception as e:
                    print(e)
                    return packinfo(infostatus=0, infomsg="数据库错误！")
                else:
                    return packinfo(infostatus=1, infomsg="题库删除成功!")
        else:
            return packinfo(infostatus=2, infomsg="没有权限!")

    @staticmethod
    def getproblemsets(token, req):
        """
        返回所有题库
        """
        if checkalltoken(token, req):
            try:
                problemsets = gdb.session.query(ProblemSet).all()
            except Exception as e:
                return packinfo(infostatus=0, infomsg="数据库错误！")
            else:
                problemlist = [x.todict() for x in problemsets]
                return packinfo(infostatus=1, inforesult=problemlist)
        else:
            return packinfo(infostatus=2, infomsg="没有权限！")

    @staticmethod
    def checkexist(token, problemsetname, req):
        """
        检查题库是否存在
        """
        if checkalltoken(token, req):
            temp = gdb.session.query(ProblemSet).filter(
                ProblemSet.problemset_title == problemsetname).first()
            if temp:
                return packinfo(infostatus=1, infomsg="题库已存在！")
            else:
                return packinfo(infostatus=0, infomsg="没有此题库！")
        else:
            return packinfo(infostatus=2, infomsg="没有权限！")

    @staticmethod
    def addproblemset(token, protitle, prodesp, req):
        """
        添加题库
        """
        print(token)
        if checkadmintoken(token, req):
            serverfilepath = os.path.join(os.getcwd(),
                                          conf.importpath, token, conf.tempfilename)
            print(serverfilepath)
            print(protitle)
            print(prodesp)
            file_zip = zipfile.ZipFile(serverfilepath, "r")
            tempdir = os.path.join(os.getcwd(), conf.importpath, token)
            for f in file_zip.namelist():
                print(tempdir)
                print(f)
                file_zip.extract(f, tempdir)
            file_zip.close()
            # os.remove(serverfilepath)
            xlsxfile = get_data_xlsx(os.path.join(os.getcwd(),
                                                  tempdir, conf.tempdirname,
                                                  conf.dataxlsxname))["题目"][1:]
            print(xlsxfile)
            psetcount = len(xlsxfile)
            protoken = gettoken()
            if len(prodesp) > 0:
                prset = ProblemSet(protitle, prodesp,
                                   psetcount, protoken, 0, 0)
                gdb.session.add(prset)
                gdb.session.commit()
            pro = gdb.session.query(ProblemSet).filter(
                ProblemSet.problemset_title == protitle).first()
            proid = pro.problemset_id
            if len(prodesp) > 0:
                actualcount = 0
            else:
                actualcount = pro.problemset_count
            for dt in xlsxfile:
                problem_desp = dt[0]
                problem_choiceA = dt[1]
                problem_choiceB = dt[2]
                problem_choiceC = dt[3]
                problem_choiceD = dt[4]
                problem_answer = dt[5]
                problem_picname = ""
                print(os.getcwd())
                if len(dt) > 6:
                    newpicname = gettoken() + "." + dt[6].rsplit(".", 1)[-1]
                    shutil.move(os.path.join(os.getcwd(), tempdir, conf.tempdirname,
                                             conf.datapicdir, dt[6]),
                                os.path.join(os.getcwd(), conf.problempicdir, newpicname))
                    problem_picname = newpicname

                """ print(problem_desp)
                print(problem_choiceA)
                print(problem_choiceB)
                print(problem_choiceC)
                print(problem_choiceD)
                print(problem_answer)
                print(problem_picname)
                print(psetcount) """

                temp = gdb.session.query(Problem).filter(and_(
                    Problem.problemset_id == proid,
                    Problem.problem_desp == problem_desp,
                    Problem.problem_choiceA == problem_choiceA,
                    Problem.problem_choiceB == problem_choiceB,
                    Problem.problem_choiceC == problem_choiceC,
                    Problem.problem_choiceD == problem_choiceD,
                    Problem.problem_answer == problem_answer
                )).first()
                if temp:
                    print("已存在的题目")
                    continue
                else:
                    pro = Problem(proid, problem_desp, problem_picname, problem_choiceA,
                                  problem_choiceB, problem_choiceC, problem_choiceD, problem_answer)
                    gdb.session.add(pro)
                    actualcount = actualcount + 1
            shutil.rmtree(tempdir)
            try:
                gdb.session.commit()
            except Exception as e:
                print(e)
                return packinfo(infostatus=0, infomsg="数据库错误！题目添加失败！")
            else:
                pro = gdb.session.query(ProblemSet).filter(
                    ProblemSet.problemset_title == protitle).first()
                pro.problemset_count = actualcount
                try:
                    gdb.session.commit()
                except Exception as e:
                    print(e)
                else:
                    return packinfo(infostatus=1, infomsg="题目添加成功！")
        else:
            return packinfo(infostatus=2, infomsg="没有权限！")

    @staticmethod
    def uploadfile(token, file, req):
        """
        添加题库文件
        """
        if checkadmintoken(token, req):
            if file and allowed_file(file.filename):
                try:
                    filename = conf.tempfilename
                    if not os.path.exists(os.path.join(os.getcwd(), conf.importpath, token)):
                        os.mkdir(os.path.join(
                            os.getcwd(), conf.importpath, token))
                    fileurl = os.path.join(
                        os.getcwd(), conf.importpath, token, filename)
                    file.save(fileurl)
                except Exception as e:
                    print(e)
                    return packinfo(infostatus=0, infomsg="目录无效，上传失败！请联系系统管理员！")
                else:
                    return packinfo(infostatus=1, infomsg="上传成功！", inforesult=fileurl)
            else:
                return packinfo(infostatus=2, infomsg="上传失败！文件格式被禁止！")
        else:
            return packinfo(infostatus=3, infomsg="没有权限！")
