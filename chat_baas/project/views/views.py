# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from flask import current_app, request
from opentracing_instrumentation.request_context import get_current_span


def list_view():
    """Example endpoint return a list of messages
    """
    current_app.logger.info("Return all messages list1")
    span = current_app.tracer.get_span(request)
    if not span:
        span = current_app.tracer.tracer.start_span(operation_name='get_messages_span', child_of=get_current_span())
    response = current_app.ms.requests.get_for_object(current_app.ms.config.service_host)
    span.log_kv({'event': 'GetData', 'value': len(response)})
    current_app.logger.info("Return all messages list2")
    return response


def create_view():
    """Example endpoint return create a messages
    """
    current_app.logger.info("Create a messages1")
    with current_app.tracer.tracer.start_span('CreateData', child_of=get_current_span()) as span:
        response = current_app.ms.requests.post_for_object(current_app.ms.config.service_host, data=request.form)
        span.log_kv({'event': 'CreateData', 'value': response})
        current_app.logger.info("Create a messages2")
    current_app.logger.info("Create a messages3")
    return response
