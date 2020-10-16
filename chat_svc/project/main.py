from __future__ import unicode_literals, print_function

import uuid

from flask import current_app, jsonify, request
from flask import session
from flask_socketio import emit, send, SocketIO
from opentracing_instrumentation import get_current_span
from pyms.flask.app import Microservice

__author__ = "Alberto Vara"
__email__ = "a.vara.1986@gmail.com"
__version__ = "0.1.0"

socketio = SocketIO()

ms = Microservice(path=__file__)
app = ms.create_app()

users_connected = []


def get_messages():
    current_app.logger.info("Return all messages list1")
    span = current_app.tracer.get_span(request)
    if not span:
        span = current_app.tracer.tracer.start_span(operation_name='get_messages_span', child_of=get_current_span())
    response = ms.requests.get_for_object(ms.config.service_host)
    span.log_kv({'event': 'GetData', 'value': len(response)})
    current_app.logger.info("Return all messages list2")
    return response


def post_message(data):
    current_app.logger.info("Create a messages1")
    with current_app.tracer.tracer.start_span('CreateData', child_of=get_current_span()) as span:
        response = ms.requests.post_for_object(ms.config.service_host, data=data)
        span.log_kv({'event': 'CreateData', 'value': response})
        current_app.logger.info("Create a messages2")
    current_app.logger.info("Create a messages3")
    return response

@app.route("/")
def index():
    return jsonify({})


@socketio.on('connect', namespace='/chat')
def on_connect():
    current_app.logger.info("USER CONNECTED")
    for msg in get_messages():
        emit('msgs', msg)


@socketio.on('log-in', namespace='/chat')
def login(data):
    user_id = session.get("user_id", "")
    if not user_id:
        user_id = str(uuid.uuid4())
        session["user_id"] = user_id
    data = {"id": user_id, "username": data.get("username", "")}

    users_connected.append(data)
    current_app.logger.info(data)
    # # Send in broadcast the actual number of connected users
    emit('users_connected', len(users_connected), broadcast=True)

    send(dict(user_id=user_id, welcome="Hola {}".format(data["username"])))


@socketio.on('disconnect', namespace='/chat')
def on_disconnect():
    # Removing the user from all the rooms where he is and broadcasting the new number
    user_id = session.get("user_id", "")
    for user in users_connected:
        if user["id"] == user_id:
            users_connected.remove(user)

    # Sending the new number of users connected
    emit('users_connected', len(users_connected), broadcast=True)


@socketio.on('send_msg', namespace='/chat')
def send_msg(data):
    # Send in broadcast the actual number of connected users

    current_app.logger.info(
        "[EVENT] User {} send message {}".format(session.get("user_id", ""), data["message"], ))
    msg = {"user_id": session.get("user_id", ""), "username": data.get("username", ""), "message": data["message"]}
    result_msg = post_message(msg)
    emit('msgs', result_msg, broadcast=True)


def create_app():
    """Initialize the Flask app, register blueprints and intialize all libraries like Swagger, database,
    the trace system...
    return the app and the database objects.
    :return:
    """
    socketio.init_app(app, logger=True, cors_allowed_origins="*")
    return app
