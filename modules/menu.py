import requests
from auth import TOKEN
import json
from datetime import datetime

dhalls = ['frary', 'frank', 'cmc', 'mudd', 'scripps', 'oldenborg', 'pitzer']
meals = ['breakfast', 'lunch', 'dinner']
days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'today']
dhall_aliases = {'collins' : 'cmc', 'colins' : 'cmc', 'hoch' : 'mudd', 'malott' : 'scripps', 'malot': 'scripps', 'oldie' : 'oldenborg', 'old' : 'oldenborg', 'mcconnel' : 'pitzer', 'mcconnell' : 'pitzer'}
day_aliases = {'m' : 'mon', 'monday' : 'mon'}

def parse_input(in_text):
    # Check each of the input words, determine what's what
    dhall = -1
    meal = -1
    day = -1
    for w in in_text:
        # Normalize the text
        w = w.lower().strip()
        for d in dhalls:
            if w in d:
                dhall = d
        for m in meals:
            if w in m:
                meal = m
        for t in days:
            if w in t:
                day = t
    # Adding compatability for dhall names (not just school name)
    # If it's still negative one, then check aliases
    if dhall is -1:
        for w in in_text:
            w = w.lower().strip()
            if w in dhall_aliases:
                dhall = dhall_aliases[w]
    return dhall, day, meal

def get_menu(dhall, day, meal):
    url = 'https://aspc.pomona.edu/api/menu/dining_hall/' + dhall + '/day/' + day + '/meal/' + meal
    req = requests.get(url , params={'auth_token' : TOKEN})
    j = json.loads(req.text)
    food = []
    food.append('~*~' + dhall + '~*~')
    food.append('~*~' + day + '~*~')
    food.append('~*~' + meal + '~*~')
    try: 
        for f in j[0]['food_items']:
            food.append(str(f))
        return food
    except:
        print("err")
        return []

def wat_meal():
    rn = datetime.now()
    if rn.hour <= 10:
        # Breakfast before 10am
        meal = 'breakfast'
    elif rn.hour > 10 and rn.hour <= 2:
        meal = 'lunch'
    else:
        meal = 'dinner'
    return meal

def menu(args):
    dhall, day, meal = parse_input(args)
    if dhall is 'mudd':
        return ('Mudd does not have their menu on the aspc site :(')
    elif dhall is not -1 and meal is not -1 and day is not -1:
        pass
    elif dhall is not -1 and meal is not -1 and day is -1:
        # No day --> default to today
        day = days[datetime.today().weekday()]
    elif dhall is not -1 and meal is -1 and day is not -1:
        # No meal --> closest meal on that day
        meal = wat_meal()
    elif dhall is -1 and meal is not -1 and day is not -1:
        # No dhall --> default to frary
        dhall = 'frary'
    elif dhall is not -1 and meal is -1 and day is -1:
        # Just dining hall --> next meal today
        meal = wat_meal()
        day = days[datetime.today().weekday()]
    elif dhall is -1 and meal is not -1 and day is -1:
        # Just meal --> default of frary today
        dhall = 'frary'
        day = days[datetime.today().weekday()]
    elif dhall is -1 and meal is -1 and day is not -1:
        # Jus the day --> frary, closest meal of that day
        dhall = 'frary'
        meal = wat_meal()
    elif dhall is -1 and meal is -1 and day is -1:
        dhall = 'frary'
        meal = wat_meal()
        day = days[datetime.today().weekday()]
    food = get_menu(dhall, day, meal)
    if len(food) > 0:
        return ('\n'.join(food))
    return "No menu"
