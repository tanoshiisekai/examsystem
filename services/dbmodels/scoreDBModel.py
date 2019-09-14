from appbase import global_db as gdb


class Score(gdb.Model):
    __tablename__ = 'score'
    score_id = gdb.Column(gdb.Integer, primary_key=True)
    user_id = gdb.Column(gdb.Integer)
    problemset_id = gdb.Column(gdb.Integer)
    score_right = gdb.Column(gdb.Integer)
    score_wrong = gdb.Column(gdb.Integer)
    score_timeduring = gdb.Column(gdb.Integer)
    score_choicelog = gdb.Column(gdb.String(1000))

    def __init__(self, user_id, problemset_id, score_right, score_wrong, score_timeduring, score_choicelog):
        self.user_id = user_id
        self.problemset_id = problemset_id
        self.score_right = score_right
        self.score_wrong = score_wrong
        self.score_timeduring = score_timeduring
        self.score_choicelog = score_choicelog

    def todict(self):
        return {"score_id": self.score_id,
                "user_id": self.user_id,
                "problemset_id": self.problemset_id,
                "score_right": self.score_right,
                "score_wrong": self.score_wrong,
                "score_timeduring": self.score_timeduring,
                "score_choicelog": self.score_choicelog}
