import flask

app = flask.Flask(__name__)

@app.route("/")
def index():
    flask.render_template("index.html")
