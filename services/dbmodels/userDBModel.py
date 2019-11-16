from appbase import global_db as gdb
class User(gdb.Model):
    __tablename__ = 'user'
    user_id = gdb.Column(gdb.Integer, primary_key=True)
    user_username = gdb.Column(gdb.String(30))
    user_password = gdb.Column(gdb.String(260))
    user_token = gdb.Column(gdb.String(260))
    user_ip = gdb.Column(gdb.String(30))
    user_logintime = gdb.Column(gdb.String(30))
    user_problemsetid = gdb.Column(gdb.Integer)
    user_problemstream = gdb.Column(gdb.String(500))
    user_problemseat = gdb.Column(gdb.Integer)
    def __init__(self, user_username,user_password,user_token,user_ip,user_logintime,user_problemsetid,user_problemstream,user_problemseat):
        self.user_username = user_username
        self.user_password = user_password
        self.user_token = user_token
        self.user_ip = user_ip
        self.user_logintime = user_logintime
        self.user_problemsetid = user_problemsetid
        self.user_problemstream = user_problemstream
        self.user_problemseat = user_problemseat
    def todict(self):
        return {"user_id":self.user_id,
"user_username":self.user_username,
"user_password":self.user_password,
"user_token":self.user_token,
"user_ip":self.user_ip,
"user_logintime":self.user_logintime,
"user_problemsetid":self.user_problemsetid,
"user_problemstream":self.user_problemstream,
"user_problemseat":self.user_problemseat}