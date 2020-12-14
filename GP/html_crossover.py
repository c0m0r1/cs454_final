#!/usr/bin/env python3

import bs4
import random
import copy
from .html_utils import get_elem_list


def swap_random_elem(t1, t2):
    elem_list1 = get_elem_list(t1)
    elem_list2 = get_elem_list(t2)
    # avoid root swap
    candidate_targets1 = [c for c in elem_list1 if c.parent is not None]
    candidate_targets2 = [c for c in elem_list2 if c.parent is not None]
    if not candidate_targets1 or not candidate_targets2: 
        return (t1, t2)

    target1 = random.choice(candidate_targets1)
    target2 = random.choice(candidate_targets2)

    target1.name, target2.name = target2.name, target1.name
    target1.attrs, target2.attrs = target2.attrs, target1.attrs

    return (t1, t2)
    
def swap_random_attr(t1, t2):
    elem_list1 = get_elem_list(t1)
    elem_list2 = get_elem_list(t2)

    candidate_targets1 = [c for c in elem_list1 if c.attrs]
    candidate_targets2 = [c for c in elem_list2 if c.attrs]
    if not candidate_targets1 or not candidate_targets2: 
        return (t1, t2)
    target1 = random.choice(candidate_targets1)
    target2 = random.choice(candidate_targets2)

    target_attr_key1 = random.choice(list(target1.attrs.keys()))
    target_attr_key2 = random.choice(list(target2.attrs.keys()))
    
    target1.attrs[target_attr_key1], target2.attrs[target_attr_key2] = target2.attrs[target_attr_key2], target1.attrs[target_attr_key1]

    return (t1, t2)

def swap_subtree(t1, t2):
    elem_list1 = get_elem_list(t1)
    elem_list2 = get_elem_list(t2)
    # avoid root swap
    target1 = random.choice([c for c in elem_list1 if c.parent is not None])
    target2 = random.choice([c for c in elem_list2 if c.parent is not None])

    target1.replace_with(copy.copy(target2))
    target2.replace_with(target1)

    return (t1, t2)
    
def swap_attr(t1, t2):
    elem_list1 = get_elem_list(t1)
    elem_list2 = get_elem_list(t2)

    candidate_targets1 = [c for c in elem_list1 if c.attrs]
    candidate_targets2 = [c for c in elem_list2 if c.attrs]
    if not candidate_targets1 or not candidate_targets2: 
        return (t1, t2)
    target1 = random.choice(candidate_targets1)
    target2 = random.choice(candidate_targets2)

    target1.attrs, target2.attrs = target2.attrs, target1.attrs

    return (t1, t2)

def crossover(t1, t2):
    operators = [
        swap_random_elem,  swap_random_attr,
        swap_subtree,      swap_attr
    ]
    return random.choice(operators)(t1, t2)


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

    t1, t2 = swap_random_elem(copy.copy(test1_soup),copy.copy(test2_soup))
    print(t1)
    print(t2)

    t1, t2 = swap_random_attr(copy.copy(test1_soup),copy.copy(test2_soup))
    print(t1)
    print(t2)
    
    t1, t2 = swap_subtree(copy.copy(test1_soup),copy.copy(test2_soup))
    print(t1)
    print(t2)

    t1, t2 = swap_attr(copy.copy(test1_soup),copy.copy(test2_soup))
    print(t1)
    print(t2)
