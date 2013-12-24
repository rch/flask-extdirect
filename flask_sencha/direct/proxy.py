import json
from datetime import datetime
from flask import Blueprint, request, abort, current_app
from api import cfg as ext_cfg
from router import doRpc, BogusAction


ext_api = Blueprint('direct', __name__)


@ext_api.route('/api', methods=['GET','POST','PUT','DELETE'])
def local_api():
    content_type = 'text/javascript'
    response_content = 'Ext.ns("Ext.app"); Ext.app.REMOTING_API = %s;' % ext_cfg()
    return current_app.response_class(response_content, mimetype=content_type)


@ext_api.route('/router', methods=['GET','POST','PUT','DELETE'])
def router():
    isForm = False;
    isUpload = False;
    if request.method != 'POST':
        response_content = json.dumps({'router':request.method})
    else:
        if request.json is not None:
            content_type = 'text/javascript'
            data = request.json   
        elif request.form.has_key('extAction'):
            isForm = True;
            isUpload = request.form['extUpload'] == 'true';
            data = BogusAction();
            data.action = request.form['extAction'];
            data.method = request.form['extMethod'];
            data.tid = request.form['extTID'] if request.form.has_key('extTID') else None # not set for upload
            data.data = [request.form, request.files]
        else:
            raise Exception('Invalid request.')
        local_response = None;
        if type(data) is list:
            local_response = []
            for datum in data:
                local_response.append(doRpc(datum))   
        else:
            local_response = doRpc(data)
        if isForm and isUpload:
            response_content = '<html><body><textarea>' 
            response_content += json.dumps(local_response)
            response_content += '</textarea></body></html>'
        else:
            response_content = json.dumps(local_response)
        
    return current_app.response_class(response_content, mimetype='application/json')

