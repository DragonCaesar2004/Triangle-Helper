import math
from os import getcwd
from itertools import permutations
from functools import lru_cache
from creating_picture import mkimg

def round(num):
    return float('{:.3f}'.format(num))


def geron(dict: dict):
    a = dict['a']
    b = dict['b']
    c = dict['c']
    if not (a >= (b + c) or b >= (a + c) or c >= (b + a)):
        p = (a + b + c) / 2
        dict['s'] = float('{:.3f}'.format(math.sqrt(p * (p - a) * (p - b) * (p - c))))
        return dict


def p(dict):
    dict['p'] = dict['a'] + dict['b'] + dict['c']
    return dict


def find_last_cor(dict, cor1, cor2, unknown_cor):
    dict[f'cor{unknown_cor}'] = 180 - dict[f'cor{cor1}'] - dict[f'cor{cor2}']
    return dict


def cor_into_cos(dict, cor):
    dict[f'cos{cor}'] = math.cos((dict[f'cor{cor}'] / 180) * math.pi)
    return dict


def cos_into_cor(dict, cos):  # own
    dict[f'cor{cos}'] = (math.acos(dict[f'cos{cos}']) * 180) / math.pi
    return dict


def cor_into_sin(dict, cor):
    dict[f'sin{cor}'] = math.sin((dict[f'cor{cor}'] / 180) * math.pi)
    return dict


def sin_into_cor(dict, sin):  # own
    dict[f'cor{sin}'] = (math.asin(dict[f'sin{sin}']) * 180 )/ math.pi
    return dict



def teor_cos(dict, name1,name2,name3):
    dict[name1]=math.sqrt((dict[name2]**2+dict[name3]**2)-(2*dict[name2]*dict[name3]*dict[f'cos{name1}']))
    return dict


def teor_sin_with_unknown_sin(dict, name1, name2):  # name2 - unknown
    dict[f'sin{name2}'] = (dict[f'sin{name1}'] * dict[name2]) / dict[name1]
    return dict


def teor_sin_with_unknown_side(dict, name1, name2):
    dict[name2] = (dict[name1] * dict[f'sin{name2}']) / (dict[f'sin{name1}'])
    return dict


def R(dict, name):
    dict['R'] = dict[name] / (dict[f'sin{name}'] * 2)
    return dict


def teor_sin_with_unknown_sin_via_R(dict, name1, name2):
    dict[f'sin{name1}'] = dict[name1] / (2 * dict['R'])
    return dict


def teor_sin_with_unknown_side_via_R(dict, name1, name2):
    dict[name1] = dict[f'sin{name1}'] * 2 * dict['R']
    return dict


def square_sah(dict, name1, name2):
    dict['s'] = 0.5 * dict[f'h{name1}'] * dict[name1]
    return dict


def find_h(dict, name1, name2):
    dict[f'h{name1}'] = dict['s'] / (0.5 * dict[name1])
    return dict


def find_side_via_sah(dict, name1, name2):
    dict[name1] = dict['s'] / (0.5 * dict[f'h{name1}'])
    return dict


def all_cors(dict, name1, name2, name3):
    dict[f'cos{name1}'] = (dict[name2] ** 2 + dict[name3] ** 2 - dict[name1] ** 2) / (2 * dict[name2] * dict[name3])
    return dict


def find_b_in_absin(dict, unknown_side, known_side, sin_known_cor):
    dict[unknown_side] = dict['s'] / (0.5 * dict[known_side] * dict[f'sin{sin_known_cor}'])
    return dict


def square_absin(dict, name1, name2, name3):
    dict['s'] = 0.5 * dict[name1] * dict[name2] * dict[f'sin{name3}']
    return dict


def sin_via_absin(dict, name1, name2, name3):
    dict[f'sin{name1}'] = dict['s'] / (0.5 * dict[name2] * dict[name3])
    return dict


def S_ab2sin(a, b, sin):  # площадь
    return (a * b * sin) / 2


def sin_ab2sin(s, a, b):
    return (s * 2) / (b * a)


def coords(dict):  # найти координаты третей точки. Если сторона А лежит на оси абцисс и берет начала от центра коорд системы
    # а сторона В продолжается по часовой
    a = dict['a']
    b = dict['b']
    c = dict['c']
    x = (b * b + a * a - c * c) / (2 * b)
    y = math.sqrt(a * a- x * x)
    return x, y

#                   side1    side2   cor
def find_bis1(dict,name1, name2, name3):
    cor1_2=dict[f'cor{name3}']/2
    cos1_2= math.cos((cor1_2 / 180) * math.pi)
    dict[f'bis{name3}']=(2*dict[name2]*dict[name1]*cos1_2)/(dict[name2]+dict[name1])
    return dict

#                   side1    side2   bis
def s_via_bis(dict,name1, name2, name3):
    one = ((dict[name1]+dict[name2])*dict[f'bis{name3}'])/(4*dict[name1]*dict[name2])
    two = math.sqrt((4*dict[name1]*dict[name1]*dict[name2]*dict[name2])-(dict[name1]+dict[name2])*(dict[name1]+dict[name2])*dict[name3]*dict[name3])
    dict['s']=one*two
#                side1    side2   side3 opposiDe
def find_med(dict,name1, name2, name3):
    a=dict[name1]
    b = dict[name2]
    c = dict[name3]
    dict[f'med{name3}']=0.5*math.sqrt(2*a**2+2*b**2-c**2)
    return dict

def find_s_via_rp(dict):
    dict['s']=(dict['p']/2)*dict['rr']
    return dict
def find_r_via_s(dict):
    dict['rr']=dict['s']/(dict['p']/2)
    return dict



def pretty_dict(dict: dict):
    for index in dict.keys():
        if dict[index]:
            dict[index] = round(dict[index])
        else:
            dict[index] = 'не найдено'
    return dict


def find_all(dict: dict):
    last_dict = dict
    while True:
        last_dict = dict
        for _ in range(7):
            dict = choice_func(dict)
        if last_dict == dict:
            dict = pretty_dict(dict)
            return dict




# @lru_cache(None)
def choice_func(dict: dict):
    names = ['a', 'b', 'c']
    if (not dict['s'] or not dict['p']) and dict['a'] and dict['b'] and dict['c']:
        dict = geron(dict)
        dict = p(dict)
    if not dict['s'] and dict['p'] and dict['rr']:
        dict=find_s_via_rp(dict)
    if not dict['rr'] and dict['p'] and dict['s']:
        dict=find_r_via_s(dict)



    for cor1, cor2, cor3 in permutations(['a', 'b', 'c']):
        if not dict[f'cor{cor3}'] and dict[f'cor{cor2}'] and dict[f'cor{cor1}']:
            dict = find_last_cor(dict, cor1, cor2, cor3)
    for name in names:
        if not dict[f'cos{name}'] and dict[f'cor{name}']:
            dict = cor_into_cos(dict, name)
        if not dict[f'cor{name}'] and dict[f'cos{name}']:
            dict = cos_into_cor(dict, name)
        if not dict[f'sin{name}'] and dict[f'cor{name}']:
            dict = cor_into_sin(dict, name)
        if not dict[f'cor{name}'] and dict[f'sin{name}']:
            dict = sin_into_cor(dict, name)

        if not dict['R'] and dict[name] and dict[f'sin{name}']:
            dict = R(dict, name)

    for name1, name2 in permutations(['a', 'b', 'c'], 2):
        if not dict[f'sin{name2}'] and dict[name2] and dict[name1] and dict[f'cor{name1}']:
            dict = teor_sin_with_unknown_sin(dict, name1, name2)
            print(name1, name2)
        if not dict[name2] and dict[f'sin{name2}'] and dict[name1] and dict[f'cor{name1}']:
            dict = teor_sin_with_unknown_side(dict, name1, name2)
        if not dict[f'sin{name1}'] and dict['R'] and dict[name1]:
            dict = teor_sin_with_unknown_sin_via_R(dict, name1, name2)
        if not dict[name1] and dict['R'] and dict[f'sin{name1}']:
            dict = teor_sin_with_unknown_side_via_R(dict, name1, name2)

        if not dict['s'] and dict[f'h{name1}'] and dict[name1]:
            dict = square_sah(dict, name1, name2)
        if not dict[f'h{name1}'] and dict['s'] and dict[name1]:
            dict = find_h(dict, name1, name2)
        if not dict[name1] and dict[f'h{name1}'] and dict['s']:
            return find_side_via_sah(dict, name1, name2)

    for name1, name2, name3 in permutations('abc'):
        if not dict[f'cos{name1}'] and dict[name1] and dict[name2] and dict[name3]:
            dict = all_cors(dict, name1, name2, name3)
        if not dict[name1] and dict['s'] and dict[f'sin{name2}'] and dict[name3]:
            dict = find_b_in_absin(dict, name1, name3, name2)  # порядок 132 НЕ МЕНЯТЬ
        if not dict['s'] and dict[name1] and dict[name2] and dict[f'sin{name3}']:
            dict = square_absin(dict, name1, name2, name3)
        if not dict[f'sin{name1}'] and dict['s'] and dict[name2] and dict[name3]:
            return sin_via_absin(dict, name1, name2, name3)
        if not dict[name1] and dict[name2] and dict[name3] and dict[f'cos{name1}']:
            return teor_cos(dict,name1,name2,name3)

        if not dict[f'bis{name3}'] and dict[name2] and dict[name1] and dict[f'cor{name3}']:
            return find_bis1(dict, name1,name2,name3)
        if not dict['s'] and dict[name1] and dict[name2] and dict[f'bis{name3}']:
            dict = s_via_bis(dict, name1, name2, name3)
        if not dict[f'med{name3}']  and dict[name1] and dict[name2] and dict[name3]:
            return find_med(dict,name1,name2,name3)


    return dict


def get_photo(dict, user_id):
    if dict['c'] and dict['a'] and dict['b']:
        x, y = coords(dict)
        return mkimg([dict['c'], dict['a'], dict['b']], x, y, user_id)
    else:
        return getcwd() + "/images/unknown.png"

def get_dict():
    return {
        'a': None,
        'b': None,
        'c': None,
        'cora': None,
        'corb': None,
        'corc': None,
        's': None,
        'R': None,
        'rr': None,
        'p': None,
        'sina': None,
        'sinb': None,
        'sinc': None,
        'cosa': None,
        'cosb': None,
        'cosc': None,
        'ha': None,
        'hb': None,
        'hc': None,
        'bisa': None,
        'bisb': None,
        'bisc': None,
        'meda': None,
        'medb': None,
        'medc': None
    }
