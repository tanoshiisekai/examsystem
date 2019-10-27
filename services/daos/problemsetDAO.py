from appbase import global_db as gdb
from dbmodels.problemsetDBModel import ProblemSet
from dbmodels.userDBModel import User
from dbmodels.problemDBModel import Problem
from sqlalchemy import and_
from tools.packtools import packinfo
from tools.auth import getmd5, gettoken, getip, gettimestr, checkusertoken, checkalltoken, checkadmintoken, allowed_file
import conf
import os
import zipfile
from pyexcel_xlsx import get_data as get_data_xlsx
import shutil
import os.path
import random


class ProblemsetDAO:

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
            if temp:
                tempdict = temp.todict()
                tempdict["problem_answer"] = getmd5(tempdict["problem_answer"])
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
                userproblemseat = 0
                firstpid = aimproblems[userproblemseat]
                user = gdb.session.query(User).filter(
                    User.user_token == token
                ).first()
                if user:
                    user.user_problemsetid = userproblemsetid
                    user.user_problemstream = userproblemstream
                    user.user_problemseat = userproblemseat
                    try:
                        gdb.session.commit()
                    except Exception as e:
                        print(e)
                        return packinfo(infostatus=0, infomsg="数据库错误!")
                    else:
                        return packinfo(infostatus=1, infomsg="初始化答题成功!", inforesult=firstpid)
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
                prset = ProblemSet(protitle, prodesp, psetcount, protoken, 0)
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
