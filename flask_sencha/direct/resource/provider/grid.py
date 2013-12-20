import sys, json, requests, flask, datetime, random, hashlib
from flask import request, session, current_app
from itertools import imap, count
from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR
from uuid import uuid4


class GridProvider(object):
    
    key = 'txn_data'
    
    def __init__(self):
        self.data = []
    
    def initialize(self):
        start_date = datetime.date.today() + datetime.timedelta(days=-90)
        end_date = datetime.date.today()
        date_range = rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO,TU,WE,TH,FR))
        num = count(1)
        session[self.key] = [{
            'id':hashlib.sha1(str(uuid4())).hexdigest(),
            'order': num.next(),
            'value':round(random.uniform(10,1000),2),
            'date':str(date),
            'checked':False,
            } for date in date_range]
    
    def items(self, params):
        if not self.key in session:
            # populate session with fake data
            self.initialize()
        self.data = session[self.key]
        if reduce(lambda x,y: x|y, imap(lambda d: 'id' in d, params)):
            self.update(params)
        return {"total": len(self.data), "data":self.data}
    
    def update(self, params):
        updates = dict((entry['id'], entry) for entry in params)
        for entry, num in zip(self.data, count()):
            if entry['id'] in updates:
                self.data[num] = updates[entry['id']]
        session[self.key] = self.data
