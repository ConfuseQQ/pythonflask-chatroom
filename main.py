import flask
import flask_login

app = flask.Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = "4e3c1a14d4b34690ac85c7c4f213869d"
users = {"confuseq": {"password": "secret"}}  # Temporary way of storing users, will be put in SQLite DB later


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    if username not in users:
        return
    user = User()
    user.id = username
    return User


@login_manager.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized", 401


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/about/")
def about():
    return flask.render_template("about.html")


@app.route("/login/", methods=("GET", "POST"))
def login():
    if flask.request.method == 'GET':
        return flask.render_template("login.html")
    username = flask.request.form["username"]
    password = flask.request.form["password"]
    if username in users and password == users[username]["password"]:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for("logged"))
    return "Bad Login"


@app.route("/loggedin/")
@flask_login.login_required
def logged():
    return flask.render_template("logged.html")


@app.route("/logout/")
def logout():
    flask_login.logout_user()
    return flask.render_template("logout.html")





if __name__ == '__main__':
    app.run(debug=True, port=6969)
