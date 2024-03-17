import flask
import flask_login
from flask_socketio import SocketIO, join_room, send, leave_room
import db_request
import random
import string


class INIT:
    app = flask.Flask(__name__)
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    app.secret_key = "4e3c1a14d4b34690ac85c7c4f213869d"
    users = db_request.get_users()
    socketio = SocketIO(app)
    rooms = {}


class User(flask_login.UserMixin):
    pass


class LOGIN:
    @staticmethod
    @INIT.login_manager.user_loader
    def user_loader(username):
        if username not in INIT.users:
            return
        user = User()
        user.id = username
        return user

    @staticmethod
    @INIT.login_manager.request_loader
    def request_loader(request):
        username = request.form.get("username")
        if username not in INIT.users:
            return
        user = User()
        user.id = username
        return User

    @staticmethod
    @INIT.login_manager.unauthorized_handler
    def unauthorized_handler():
        return "Unauthorized", 401

    @staticmethod
    @INIT.app.route("/login/", methods=["GET", "POST"])
    def login():
        if flask.request.method == "GET":
            return flask.render_template("login.html")
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")
        if username in INIT.users and password == db_request.get_password(username):
            user = User()
            user.id = username
            flask_login.login_user(user)
            return flask.redirect(flask.url_for("userpanel"))
        return "Bad Login"


class USERAPP:

    @staticmethod
    def generate_unique_code(lenght):
        while True:
            code = ""
            for _ in range(lenght):
                code += random.choice(string.ascii_uppercase)
            if code not in INIT.rooms:
                break
        return code

    @staticmethod
    @INIT.app.route("/")
    @INIT.app.route("/home/")
    def index():
        return flask.render_template("index.html")

    @staticmethod
    @INIT.app.route("/userpanel/")
    @flask_login.login_required
    def userpanel():
        user = flask_login.current_user.id
        return flask.render_template("userpanel.html", username=user)

    @staticmethod
    @INIT.app.route("/hub/", methods=["POST", "GET"])
    @flask_login.login_required
    def hub():
        if flask.request.method == "POST":
            # name = flask_login.current_user.id
            code = flask.request.form.get("code")
            join = flask.request.form.get("join", False)
            create = flask.request.form.get("create", False)
            if join is not False and not code:
                return flask.render_template("chatroom_hub.html", error="Code is required", code=code)
            room = code
            if create is not False:
                room = USERAPP.generate_unique_code(4)
                INIT.rooms[room] = {"members": 0, "messages": []}
            elif code not in INIT.rooms:
                return flask.render_template("chatroom_hub.html", error="Room does not exist", code=code)
            flask.session["room"] = room
            return flask.redirect(flask.url_for("room"))
        return flask.render_template("chatroom_hub.html")

    @staticmethod
    @flask_login.login_required
    @INIT.app.route("/room/")
    def room():
        room = flask.session.get("room")
        if room is None or room not in INIT.rooms:
            return flask.redirect(flask.url_for("hub"))

        return flask.render_template("room.html")

    @staticmethod
    @flask_login.login_required
    @SocketIO.on("SocketIO", message="connect")
    def connect():
        room = flask.request.args.get("room")
        name = flask_login.current_user.id
        if not room or not name:
            return
        if room not in INIT.rooms:
            leave_room(room)
            return
        join_room(room)
        send({"name": name, "message": "has entered the room"}, to=room)
        INIT.rooms[room]["members"] += 1
        print(f"{name} has entered the room {room}")

    @staticmethod
    @SocketIO.on(message="disconnect")
    @flask_login.login_required
    def disconnect():
        room = flask.request.args.get("room")
        name = flask_login.current_user.id
        join_room(room)
        if room in INIT.rooms:
            INIT.rooms[room]["members"] -= 1
            if INIT.rooms[room]["members"] <= 0:
                del INIT.rooms[room]
        send({"name": name, "message": "has left the room"}, to=room)
        print(f"{name} has left the room {room}")

    @staticmethod
    @INIT.app.route("/logout/")
    def logout():
        flask_login.logout_user()
        return flask.redirect(flask.url_for("index"))


if __name__ == '__main__':
    INIT.app.run(debug=True, port=6969)
