from appbase import global_db as gdb
class NoteBook(gdb.Model):
    __tablename__ = 'notebook'
    notebook_id = gdb.Column(gdb.Integer, primary_key=True)
    user_id = gdb.Column(gdb.Integer)
    problemset_id = gdb.Column(gdb.Integer)
    problem_id = gdb.Column(gdb.Integer)
    def __init__(self, user_id,problemset_id,problem_id):
        self.user_id = user_id
        self.problemset_id = problemset_id
        self.problem_id = problem_id
    def todict(self):
        return {"notebook_id":self.notebook_id,
"user_id":self.user_id,
"problemset_id":self.problemset_id,
"problem_id":self.problem_id}