from appbase import global_db as gdb


class Score(gdb.Model):
    __tablename__ = 'score'
    score_id = gdb.Column(gdb.Integer, primary_key=True)
    user_id = gdb.Column(gdb.Integer)
    problemset_id = gdb.Column(gdb.Integer)
    score_right = gdb.Column(gdb.Integer)
    score_wrong = gdb.Column(gdb.Integer)
    score_timestart = gdb.Column(gdb.Integer)
    score_timeend = gdb.Column(gdb.Integer)
    score_problemcount = gdb.Column(gdb.Integer)
    problemset_timeperproblem = gdb.Column(gdb.Integer)

    def __init__(self, user_id, problemset_id, score_right, score_wrong, score_timestart, score_timeend, score_problemcount, problemset_timeperproblem):
        self.user_id = user_id
        self.problemset_id = problemset_id
        self.score_right = score_right
        self.score_wrong = score_wrong
        self.score_timestart = score_timestart
        self.score_timeend = score_timeend
        self.score_problemcount = score_problemcount
        self.problemset_timeperproblem = problemset_timeperproblem

    def todict(self):
        return {"score_id": self.score_id,
                "user_id": self.user_id,
                "problemset_id": self.problemset_id,
                "score_right": self.score_right,
                "score_wrong": self.score_wrong,
                "score_timestart": self.score_timestart,
                "score_timeend": self.score_timeend,
                "score_problemcount": self.score_problemcount,
                "problemset_timeperproblem": self.problemset_timeperproblem}
