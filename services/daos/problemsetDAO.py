from appbase import global_db as gdb
from dbmodels.problemsetDBModel import ProblemSet
from dbmodels.problemDBModel import Problem
from sqlalchemy import and_
from tools.packtools import packinfo
from tools.auth import gettoken, getip, gettimestr, checktoken, allowed_file
import conf
import os
import zipfile
from pyexcel_xlsx import get_data as get_data_xlsx
import shutil
import os.path


class ProblemsetDAO:

    @staticmethod
    def getproblemsets(token):
        """
        返回所有题库
        """
        if checktoken(token):
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
    def checkexist(token, problemsetname):
        """
        检查题库是否存在
        """
        if checktoken(token):
            temp = gdb.session.query(ProblemSet).filter(
                ProblemSet.problemset_title == problemsetname).first()
            if temp:
                return packinfo(infostatus=1, infomsg="题库已存在！")
            else:
                return packinfo(infostatus=0, infomsg="没有此题库！")
        else:
            return packinfo(infostatus=2, infomsg="没有权限！")

    @staticmethod
    def addproblemset(token, protitle, prodesp):
        """
        添加题库
        """
        print(token)
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
            tempdir, conf.tempdirname, conf.dataxlsxname))["题目"][1:]
        print(xlsxfile)
        psetcount = len(xlsxfile)
        protoken = gettoken()
        if len(prodesp) > 0:
            prset = ProblemSet(protitle, prodesp, psetcount, protoken)
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
                shutil.move(os.path.join(os.getcwd(), tempdir, conf.tempdirname, conf.datapicdir, dt[6]),
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

    @staticmethod
    def uploadfile(token, file):
        """
        添加题库文件
        """
        if checktoken(token):
            if file and allowed_file(file.filename):
                try:
                    filename = conf.tempfilename
                    if not os.path.exists(os.path.join(os.getcwd(), conf.importpath, token)):
                        os.mkdir(os.path.join(os.getcwd(), conf.importpath, token))
                    fileurl = os.path.join(os.getcwd(), conf.importpath, token, filename)
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
