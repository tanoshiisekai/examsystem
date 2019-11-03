from appbase import global_db as gdb


class Problem(gdb.Model):
    __tablename__ = 'problem'
    problem_id = gdb.Column(gdb.Integer, primary_key=True)
    problemset_id = gdb.Column(gdb.Integer)
    problem_desp = gdb.Column(gdb.String(1000))
    problem_picpath = gdb.Column(gdb.String(300))
    problem_choiceA = gdb.Column(gdb.String(200))
    problem_choiceB = gdb.Column(gdb.String(200))
    problem_choiceC = gdb.Column(gdb.String(200))
    problem_choiceD = gdb.Column(gdb.String(200))
    problem_answer = gdb.Column(gdb.String(10))

    def __init__(self, problemset_id, problem_desp, problem_picpath, problem_choiceA, problem_choiceB, problem_choiceC, problem_choiceD, problem_answer):
        self.problemset_id = problemset_id
        self.problem_desp = problem_desp
        self.problem_picpath = problem_picpath
        self.problem_choiceA = problem_choiceA
        self.problem_choiceB = problem_choiceB
        self.problem_choiceC = problem_choiceC
        self.problem_choiceD = problem_choiceD
        self.problem_answer = problem_answer

    def todict(self):
        return {"problem_id": self.problem_id,
                "problemset_id": self.problemset_id,
                "problem_desp": self.problem_desp,
                "problem_picpath": self.problem_picpath,
                "problem_choiceA": self.problem_choiceA,
                "problem_choiceB": self.problem_choiceB,
                "problem_choiceC": self.problem_choiceC,
                "problem_choiceD": self.problem_choiceD,
                "problem_answer": self.problem_answer}
