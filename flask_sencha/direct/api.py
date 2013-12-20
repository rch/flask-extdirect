import json
from config import API
from flask import request, url_for

def cfg():
    # convert API config to Ext.Direct spec
    actions = {}
    for aname, a in API.iteritems():
        methods = []
        for mname, m in a['methods'].iteritems():
            if m.has_key('len'):
                md = {
                    'name': mname,
                    'len': m['len']
                }
            else:
                md = {
                    'name': mname,
                    'params': m['params']
                }
            if m.has_key('formHandler') and m['formHandler']:
                md['formHandler'] = True
            methods.append(md)
        actions[aname] = methods
    
    return json.dumps({
        'url': request.url_root.rstrip('/') + url_for('direct.router'),
        'type': 'remoting',
        'actions': actions
    })
