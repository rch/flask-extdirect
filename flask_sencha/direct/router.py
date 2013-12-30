import resource
import message
from message import DirectRequest
from config import API
from flask import request, session, current_app

class BogusAction(dict):
    """ 
        sub-classes dict to support mixed usage left over from the 
        original implementation in router.php from Sencha... 
    """  
    
    def __init__(self):
        self['action'] = None
        self['method'] = None 
        self['data'] = None
        self['tid'] = None
        
    def __getattr__(self, key):
        return self[key]
        
    def __setattr__(self, key, value):
        self[key] = value 


def something(cdata):
    if type(cdata) is not DirectRequest:
        # log deprecated call (we shouldn't be parsing here)
        # this creates a Message from cdata
        msg = message.parse(cdata)
    else:
        msg = cdata
    
    if not API.has_key(msg.name):
        raise Exception('Call to undefined action: ' . msg.name)
    
    # grabs the name of the action - 
    a = API[msg.name]
    
    # doAroundCalls(a['before'], cdata)
    
    mdef = a['methods'][msg.method]
    if not mdef:
        raise Exception("Call to undefined method: %s on action %" % (msg.method, msg.name))

    r = {
        'type': msg.type,
        'tid': msg.tid,
        'action': msg.name,
        'method': msg.method
    }

    cls = getattr(resource, msg.name)
    o = cls()
    
    if mdef.has_key('len'):
        params = cdata['data'] if cdata.has_key('data') and type(cdata['data']) is list else []
    else:
        if type(cdata) is dict:
            params = cdata
        else:
            params = [cdata.data]
    
    fn = getattr(o, msg.method)
    r['result'] = fn(params)

    return r;

    