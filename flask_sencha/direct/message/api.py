from collections import namedtuple
from itertools import izip, tee
import directrpc_pb2
from directrpc_pb2 import Message, Item, Action, Range
import action

DirectRequest = namedtuple('DirectRequest', ['action','type','tid','data','method'])

# this poor, inefficient method is just a placeholder
# that will provide sufficient functionality while I'm
# focusing on other aspects of the package   
def parse(cdata):
    assert type(cdata) is dict
    try:
        req = DirectRequest(**cdata)
    except TypeError as e:
        # TODO log unknown fields
        raise e
    msg = Message()
    tmp = msg.action.add()
    tmp.name = req.action
    tmp.method = req.method
    tmp.type = req.type
    tmp.tid = req.tid
    list_iterator = iter(action.data.types)
    for data, types in izip(req.data, tee(list_iterator)):
        try:
            found = False
            while not found:
                chk = types.next()
                try:
                    value = chk(**data) # raises TypeError
                    property_name = chk.__name__
                    tmp.data.append(property_name.lower())
                    property = getattr(tmp, property_name.lower()).add()
                    for field_name in value._fields:
                        setattr(property, field_name, getattr(value, field_name))
                    found = True
                except TypeError:
                    pass # keep going until we find the right type
        except StopIteration as e:
            # TODO log unknown data format
            print data
            raise e
    return tmp
