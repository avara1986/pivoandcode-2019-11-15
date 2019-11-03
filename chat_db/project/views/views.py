# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from flask import jsonify, current_app, request

from project.models.init_db import db
from project.models.models import Message
from opentracing_instrumentation.request_context import get_current_span


def list_view():
    """Example endpoint return a list of messages
    """
    span = current_app.tracer.get_span(request)
    current_app.logger.info("Return all messages list1")
    current_app.logger.info("Return all messages list2")
    query = Message.query.all()
    span.log_kv({'event': 'ListAction', 'value': len(query)})
    current_app.logger.info("Return all messages list3")

    current_app.logger.info("Return all messages list4")
    return jsonify([i.serialize for i in query])


def create_view():
    """Example endpoint return create a messages
    """
    current_app.logger.info("Create messages1")
    span = current_app.tracer.get_span(request)
    current_app.logger.info("Create messages2")
    object_db = Message(**{
        "user_id": request.form["user_id"],
        "username": request.form["username"],
        "message": request.form["message"]
    })
    span.log_kv({'event': 'CreateAction', 'value': object_db.user_id})
    span.log_kv({'event': 'span id', 'value': span.context.trace_id})
    current_app.logger.info("Create messages3")
    db.session.add(object_db)
    db.session.commit()
    current_app.logger.info("Create messages4")

    return jsonify(object_db.serialize)
