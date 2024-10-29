import math

from pyswip import Prolog

# Инициализация Prolog
prolog = Prolog()

def who_is_faster(T1, T2):
    p_query = f'faster({T1}, {T2}).'
    is_faster = len(list(prolog.query(p_query))) == 1
    return T2 if is_faster else T1

def who_is_faster_than(T1):
    p_query = f'faster({T1}, T).'
    tanks = [i['T'] for i in list(prolog.query(p_query))]
    return ', '.join(map(str, tanks)) + f' are faster than {T1}'

def who_is_protected(T1, T2):
    p_query = f'protected({T1}, {T2}).'
    is_protected = len(list(prolog.query(p_query))) == 1
    return T2 if is_protected else T1

def who_is_protected_than(T1):
    p_query = f'protected({T1}, T).'
    tanks = [i['T'] for i in list(prolog.query(p_query))]
    return ', '.join(tanks) + f' are more protected than {T1}'


def how_can_get(T1):
    p_query = f'upgrade(T, {T1}, _).'
    tanks = [i['T'] for i in list(prolog.query(p_query))]
    tanks = sorted(tanks, key=get_level)
    return ' > '.join(tanks)


def get_level(T1):
    p_query = f'level({T1}, L).'
    return int(next(prolog.query(p_query))['L'])


def get_tanks_type(types):
    p_query = ' ; '.join([f'{i}(T)' for i in types])
    return [i['T'] for i in list(prolog.query(p_query))]


def like_speed(is_like):
    is_like = is_like is None
    if is_like:
        return get_tanks_type(['light', 'medium'])
    else:
        return get_tanks_type(['heavy', 'medium'])


def like_defence_or_dmg(is_like):
    is_like = is_like is None
    if is_like:
        return get_tanks_type(['heavy', 'medium'])
    else:
        return get_tanks_type(['light', 'medium'])


def have_exp(exp, r=1, a=35):
    # https://www.desmos.com/calculator/okoisxepsw
    exp_to_lvl = lambda x: (1 / (1 + math.exp(- x / a)) - 0.5) * 20
    lvl = round(exp_to_lvl(int(exp)))
    p_query = f'level(T, Lvl) , abs(Lvl - {lvl}) < {r + 1}.'
    tanks = [i['T'] for i in prolog.query(p_query)]
    return tanks

def want_to_win(T, r = 2):
    cur_lvl = get_level(T)
    p_query = f'level(T, Lvl) , Lvl > {cur_lvl}, {cur_lvl + r + 1} > Lvl.'
    tanks = [i['T'] for i in prolog.query(p_query)]
    return tanks
