__author__ = 'Alexey Kutepov'

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_at_index(list, index):
    return list[index]


@register.filter
def to_class_name(value):
    return value.__class__.__name__


@register.filter
def index(List, i):
    return List[int(i)]


@register.filter
def get_answers_by_index(List, i):
    list = []
    if type(List[int(i)].get_answer()) == str:
        list.append(int(List[int(i)].get_answer()))
    else:
        for item in List[int(i)].get_answer():
            list.append(int(item))
    return list

@register.filter
def get_answer_by_index(List, i):
    return List[int(i)].get_answer()

@register.filter
def is_correct_by_index(List, i):
    return List[int(i)].is_correct()