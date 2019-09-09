from appbase import global_db as gdb


class ProblemSet(gdb.Model):
    __tablename__ = 'problemset'
    problemset_id = gdb.Column(gdb.Integer, primary_key=True)
    problemset_desp = gdb.Column(gdb.String(300))
    problemset_count = gdb.Column(gdb.Integer)

    def __init__(self, problemset_id, problemset_desp, problemset_count):
        self.problemset_id = problemset_id
        self.problemset_desp = problemset_desp
        self.problemset_count = problemset_count

    def todict(self):
        return {"problemset_id": self.problemset_id,
                "problemset_desp": self.problemset_desp,
                "problemset_count": self.problemset_count}
