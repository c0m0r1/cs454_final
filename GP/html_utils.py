#!/usr/bin/env python3

import bs4


def get_elem_list(t):
    if not t.contents: return [t]
    root = t.contents[0]
    res_li = []
    for child in t.children:
        if not isinstance(child, bs4.element.NavigableString): 
            res_li += get_elem_list(child)
    
    return [t] + res_li
