import flask
import flask.sessions
import flask_session

app = flask.Flask(__name__)
app.secret_key = "b9b675549c474e52fa975baca0fb68663074e4439f0b981d1c63aeede9de06e1"
app.config["SESSION_TYPE"] = "filesystem"
flask_session.Session(app)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/about/")
def about():
    return flask.render_template("about.html")


@app.route("/login/")
def login():
    #if request.method == 'POST':
    #    pass
    #else:
    #    return flask.render_template("login.html")
    return flask.render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True, port=6969)
