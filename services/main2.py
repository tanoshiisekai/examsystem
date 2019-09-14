from flask import Flask, send_file
from io import BytesIO
from urllib.parse import quote
import conf

app = Flask(__name__)


@app.route("/gettemplate/", methods=["GET"])
def download():
    out = BytesIO()
    filedir = conf.filebasedir + "/" + conf.filebasefilename
    with open(filedir, "rb") as fp:
        out.write(fp.read())
    filename = quote(conf.filebasefilename)
    out.seek(0)
    rv = send_file(out, as_attachment=True, attachment_filename=filename)
    rv.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(
        filename)
    return rv


if __name__ == "__main__":
    app.debug = True
    app.run(host=conf.fileserverip, port=conf.fileserverport)
