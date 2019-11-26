from daos.initDAO import InitDAO
from tools.auth import getmd5


InitDAO.insertadmin("long", getmd5("testlong"))
InitDAO.insertsettings("togglenotebook", "1")   # 默认打开错题本

