import data
from .. import resource

__all__ = ['data']

def create_from(message):
    Action = getattr(resource, message.name)
    return Action(message)
