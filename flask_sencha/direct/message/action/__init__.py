import os, sys
from ... import resource

def create_from(message, cdata):
    Action = getattr(resource, message.name)
    return Action(message, cdata)
