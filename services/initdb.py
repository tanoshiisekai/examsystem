from daos.adminloginDAO import AdminloginDAO
from tools.auth import getmd5


AdminloginDAO.insert("admin", getmd5("longlong"))

