from appbase import global_db as gdb
import dbmodels


def create_db():
    gdb.create_all()
    
