from appbase import global_db as gdb
class Admin(gdb.Model):
    __tablename__ = 'admin'
    admin_id = gdb.Column(gdb.Integer, primary_key=True)
    admin_username = gdb.Column(gdb.String(30))
    admin_password = gdb.Column(gdb.String(260))
    admin_token = gdb.Column(gdb.String(260))
    admin_ip = gdb.Column(gdb.String(30))
    admin_logintime = gdb.Column(gdb.String(30))
    def __init__(self, admin_username,admin_password,admin_token,admin_ip,admin_logintime):
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.admin_token = admin_token
        self.admin_ip = admin_ip
        self.admin_logintime = admin_logintime
    def todict(self):
        return {"admin_id":self.admin_id,
"admin_username":self.admin_username,
"admin_password":self.admin_password,
"admin_token":self.admin_token,
"admin_ip":self.admin_ip,
"admin_logintime":self.admin_logintime}