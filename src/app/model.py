import random as rnd
import datetime as dt
import string

def random_text():
    return "".join( [rnd.choice(string.ascii_letters) for i in range(45)] )

def random_date():
    delta = dt.datetime.strptime('1/1/2022 1:30 PM', '%m/%d/%Y %I:%M %p') - dt.datetime.strptime('1/1/2000 1:30 PM', '%m/%d/%Y %I:%M %p')
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = rnd.randrange(int_delta)
    return dt.datetime.strptime('1/1/2000 1:30 PM', '%m/%d/%Y %I:%M %p') + dt.timedelta(seconds=random_second)

def run(query: str):
    results = []
    for i in range(rnd.randint(1, 10)):
        results.append({
            'name': "Kanun " + str(rnd.randint(1, 100)),
            'date': random_date(),
            'number': rnd.randint(1, 100),
            'info': random_text()
            })
    return results