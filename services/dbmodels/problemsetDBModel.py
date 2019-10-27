from appbase import global_db as gdb
class ProblemSet(gdb.Model):
    __tablename__ = 'problemset'
    problemset_id = gdb.Column(gdb.Integer, primary_key=True)
    problemset_title = gdb.Column(gdb.String(100))
    problemset_desp = gdb.Column(gdb.String(300))
    problemset_count = gdb.Column(gdb.Integer)
    problemset_token = gdb.Column(gdb.String(260))
    problemset_answercount = gdb.Column(gdb.Integer)
    def __init__(self, problemset_title,problemset_desp,problemset_count,problemset_token,problemset_answercount):
        self.problemset_title = problemset_title
        self.problemset_desp = problemset_desp
        self.problemset_count = problemset_count
        self.problemset_token = problemset_token
        self.problemset_answercount = problemset_answercount
    def todict(self):
        return {"problemset_id":self.problemset_id,
"problemset_title":self.problemset_title,
"problemset_desp":self.problemset_desp,
"problemset_count":self.problemset_count,
"problemset_token":self.problemset_token,
"problemset_answercount":self.problemset_answercount}