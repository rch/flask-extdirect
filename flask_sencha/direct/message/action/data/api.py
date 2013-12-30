from collections import namedtuple

Item = namedtuple('Item', ['date','id','checked','value','order'])

Range = namedtuple('Range', ['start','limit','page'])    

types = [Item, Range]
