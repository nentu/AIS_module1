from QueryCreator import Query
from query_func import *

# Загружаем базу знаний из файла
prolog.consult("knowledge_base.pl")  # Убедитесь, что путь к файлу правильный

'''
Search

Who is faster {T1} or {T2} | T1 or T2
Who is faster than {T1} | tank_list

Who is more protected {T1} or {T2} | T1 or T2
Who is more protected than {T1} | tank_list

Who can I get {T1} | T1 > T2 > T3 > ...

What level is {T1} | Lvl

RecSys

Recommend a tank:
I (like/dislike) speed
I (like/dislike) defense
I (like/dislike) damage

I have N hours of experience in the game.
I want to win {T}
'''

query_list = [
    Query('What level is (\S+)', get_level),
    Query('Who can I get (\S+)', how_can_get),

    Query('Who is faster (\S+) or (\S+)', who_is_faster),
    Query('Who is faster than (\S+)', who_is_faster_than),

    Query('Who is more protected (\S+) or (\S+)', who_is_protected),
    Query('Who is more protected than (\S+)', who_is_protected_than),

]

rec_query_list = [
    Query('I (dis)?like speed', like_speed),
    Query('I (dis)?like defence', like_defence_or_dmg),
    Query('I (dis)?like damage', like_defence_or_dmg),

    Query('I have (\d+) hours of experience in the game.', have_exp),

    Query('I want to win (\S+)', want_to_win),
]

query = 'Bla' + 'I want to win blackPrince ' + 'Bla'


def get_resp(query):
    for q in query_list:
        resp = q.resp(query)
        if resp is None:
            continue

        print(resp)
        break
    else:
        print('No query found')


def get_all_tanks():
    p_query = f'light(T) ; medium(T) ; heavy(T)'
    tanks = [i['T'] for i in list(prolog.query(p_query))]
    return tanks


ALL_TANKS_SET = set(get_all_tanks())


def get_rec():
    cur_set = ALL_TANKS_SET.copy()
    query = ''
    while query != 'thnx':
        query = input('- ')
        for q in rec_query_list:
            resp = q.resp(query)
            if resp is None:
                continue

            print(f'Tanks for current request:\n\t' + '\n\t'.join(resp))
            cur_set &= set(resp)
            print('-' * 10)
            print(f'Tanks for you:\n\t' + '\n\t'.join(cur_set))

            break
        else:
            return 'No query found'


while True:
    query = input('- ')

    if query == 'end':
        break

    if 'recommend' in query:
        print('Ok, Get more info about your preferences')
        get_rec()
        continue
    get_resp(query)

print('Bye')
