import resource
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


def doRpc(cdata):
    
    if not API.has_key(cdata['action']):
        raise Exception('Call to undefined action: ' . cdata.action)
    
    action = cdata['action']
    a = API[action]

    # doAroundCalls(a['before'], cdata)

    method = cdata['method']
    mdef = a['methods'][method]
    if not mdef:
        raise Exception("Call to undefined method: %s on action %" % (method, action))
    
    # doAroundCalls(mdef['before'], cdata);

    r = {
        'type': 'rpc',
        'tid': cdata['tid'],
        'action': action,
        'method': method
    }

    cls = getattr(resource, action)
    o = cls()
    
    if mdef.has_key('len'):
        params = cdata['data'] if cdata.has_key('data') and type(cdata['data']) is list else []
    else:
        if type(cdata) is dict:
            params = cdata
        else:
            params = [cdata.data]
    
    fn = getattr(o, method)
    r['result'] = fn(params)

    # doAroundCalls(mdef['after'], cdata, r);
    # doAroundCalls(a['after'], cdata, r);
    
    """
    except Exception as e:
        
        r = {}
        r['type'] = 'exception';
        r['message'] = str(e)
        r['where'] = 'server.direct.router'
    """
    return r;



def doAroundCalls(fns, cdata, returnData=None):
    if not fns:
        return
    
    if type(fns) is list:
        for fn in fns:
            fn(cdata, returnData)
    else:
        fns(cdata, returnData)

    