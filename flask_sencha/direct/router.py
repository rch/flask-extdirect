import action
import resource
import message
from message import DirectRequest, DirectResponse, make_response
from config import API
from flask import request, session, current_app


def something(cdata):
    if type(cdata) is not DirectRequest:
        # log deprecated call (we shouldn't be parsing here)
        # this creates a Message from cdata
        msg = message.parse(cdata)
        # attach a reference to cdata sine we're not handling 
        # params from the real message yet
        msg.cdata = cdata
    else:
        msg = cdata
    
    delegate = action.create_from(msg)
    
    return make_reponse(cdata, delegate())
