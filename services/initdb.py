from daos.initDAO import InitDAO
from tools.auth import getmd5


InitDAO.insertadmin("long", getmd5("testlong"))
InitDAO.insertsettings("togglenotebook", "0")   # 默认关闭错题本


