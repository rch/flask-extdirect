import message, resource
from message import action
from message.api import make_response, DirectRequest, DirectResponse 
from flask import request, session, current_app


def something(cdata):
    if type(cdata) is not DirectRequest:
        # log deprecated call (we shouldn't be parsing here)
        # this creates a Message from cdata
        msg = message.parse(cdata)
    else:
        msg = cdata
    
    delegate = action.create_from(msg, cdata)
    
    return make_response(cdata, delegate(cdata))
