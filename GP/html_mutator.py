#!/usr/bin/env python3

import bs4
import random
import copy
from html_constants import TAGS, ATTRS
from html_utils import get_elem_list


def delete_random_elem(t):
    elem_list = get_elem_list(t)
    # avoid root deletion && empty-content tags
    candidate_target = [c for c in elem_list if c.parent is not None]
    if not candidate_target : return t
    target = random.choice(candidate_target)
    
    candidate_target_child = [c for c in target.children if not isinstance(c, bs4.element.NavigableString)]
    if not candidate_target_child:
        if not target.contents:
            target.extract()
            return t
        # pick arbitrary child and discard left
        target_child = random.choice(target.contents)
        left_childs = []
    else:
        target_child = random.choice(candidate_target_child)
        left_childs = list(target_child.next_siblings) + list(target_child.previous_siblings)
    
    target.replace_with(target_child)
    for c in left_childs:
        target_child.append(c)
    
    return t

def add_random_elem(t):
    elem_list = get_elem_list(t)
    
    target = random.choice(elem_list)
    new_elem = t.new_tag(random.choice(TAGS))
    
    if not target.contents:
        target.insert(0, new_elem)
    else:
        target.insert(random.randrange(len(target.contents)), new_elem)

    return t

def replace_random_elem(t):
    elem_list = get_elem_list(t)
    
    target = random.choice(elem_list)
    target.name = random.choice(TAGS)

    return t

def shuffle_random_elem(t):
    elem_list = get_elem_list(t)
    
    candidate_target = [c for c in elem_list if len(c.contents) > 1]

    if not candidate_target: return t
    random.shuffle(random.choice(candidate_target).contents)

    return t

def delete_random_attr(t):
    elem_list = get_elem_list(t)

    candidate_targets = [c for c in elem_list if c.attrs]
    # no elem to shuffle
    if not candidate_targets: return t
    target = random.choice(candidate_targets)
    target_attr_key = random.choice(list(target.attrs.keys()))

    del target[target_attr_key]

    return t

def add_random_attr(t):
    elem_list = get_elem_list(t)
    
    target = random.choice(elem_list)
    # TODO : add more various attr value
    target[random.choice(ATTRS)] = random.randrange(256)

    return t

def replace_random_attr(t):
    elem_list = get_elem_list(t)

    candidate_targets = [c for c in elem_list if c.attrs]

    if not candidate_targets: return t
    target = random.choice(candidate_targets)
    target_attr_key = random.choice(list(target.attrs.keys()))

    target[random.choice(ATTRS)] = target[target_attr_key]
    del target[target_attr_key]

    return t

def inject_byte(t):
    t_str = list(str(t))
    # TODO : is there more various (and effective) byte injection method?
    # ex) do not re-interprete with bs and directly evaluate fitness
    t_str[random.randrange(len(t_str))] = chr(random.randrange(256))
    return bs4.BeautifulSoup("".join(t_str), "lxml", multi_valued_attributes=None)

def mutate(t):
    mutators = [
        delete_random_elem,  add_random_elem,
        replace_random_elem, shuffle_random_elem,
        delete_random_attr,  add_random_attr,
        replace_random_attr, inject_byte
    ]
    return random.choice(mutators)(t)


if __name__=="__main__":
    test1 = """<html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p></body></html>"""

    test2 = """<html><head><title>HTML Test Suite: n.0 Section Title</title>
    <meta http-equiv="Content-Style-Type" content="text/css">
    <link rel="stylesheet" type="text/css" media="screen" href="static.css">
    </head>
    <body class="navigation">
    <h2>HTML4 Test Suite: n.0 Section Title</h2>
    <hr>
    <p>
    In this section:
    </p>
    <ul>
    <li><a href="secTestName1.html">Test secTestName1.html</a></li>
    <li><a href="secTestName2.html">Test secTestName2.html</a></li>
    <li><a href="secTestName3.html">Test secTestName3.html</a></li>
    <li><a href="secTestName4.html">Test secTestName4.html</a></li>
    <li><a href="secTestName5.html">Test secTestName5.html</a></li>
    <li><a href="secTestName6.html">Test secTestName6.html</a></li>
    <li> <a href="secTestName7.html">Test secTestName7.html</a></li>
    </ul>
    <hr>
    <br>
    </body></html>"""

    #didn't consider multi_valued_attributes
    test1_soup = bs4.BeautifulSoup(test1, "lxml", multi_valued_attributes=None)
    test2_soup = bs4.BeautifulSoup(test2, "lxml", multi_valued_attributes=None)

    print(delete_random_elem(copy.copy(test1_soup)))
    print(add_random_elem(copy.copy(test1_soup)))
    print(replace_random_elem(copy.copy(test1_soup)))
    print(shuffle_random_elem(copy.copy(test1_soup)))
    print(delete_random_attr(copy.copy(test1_soup)))
    print(add_random_attr(copy.copy(test1_soup)))
    print(replace_random_attr(copy.copy(test1_soup)))

    print(delete_random_elem(copy.copy(test2_soup)))
    print(add_random_elem(copy.copy(test2_soup)))
    print(replace_random_elem(copy.copy(test2_soup)))
    print(shuffle_random_elem(copy.copy(test2_soup)))
    print(delete_random_attr(copy.copy(test2_soup)))
    print(add_random_attr(copy.copy(test2_soup)))
    print(replace_random_attr(copy.copy(test2_soup)))
