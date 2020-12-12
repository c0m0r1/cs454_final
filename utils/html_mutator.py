#!/usr/bin/env python3

import bs4
import random
import copy

# from https://stackoverflow.com/questions/2439374/where-to-find-a-list-of-all-the-possible-html-tags-in-python
# we can use one in domato or DOMpurify instead
# TODO : update if need more tags
TAGS = ["a","abbr","acronym","address","area","b","base","bdo","big","blockquote","body","br","button","caption","cite","code","col","colgroup","dd","del","dfn","div","dl","DOCTYPE","dt","em","fieldset","form","h1","h2","h3","h4","h5","h6","head","html","hr","i","img","input","ins","kbd","label","legend","li","link","map","meta","noscript","object","ol","optgroup","option","p","param","pre","q","samp","script","select","small","span","strong","style","sub","sup","table","tbody","td","textarea","tfoot","th","thead","title","tr","tt","ul","var"]

# but attrs are too tag-aware and type sensative...
# maybe we should use grammer of domato for better result
# for now i use some attrs from https://www.w3schools.com/tags/ref_standardattributes.asp
# TODO : update if need more atrrs
ATTRS = ["accesskey", "class", "contenteditable", "dir", "hidden", "draggable", "lang", "style", "title", "translate"]

def get_elem_list(t):
    if not t.contents: return [t]
    root = t.contents[0]
    res_li = []
    for child in t.children:
        if not isinstance(child, bs4.element.NavigableString): 
            res_li += get_elem_list(child)
    
    return [t] + res_li

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
    return bs4.BeautifulSoup("".join(t_str), "lxml",multi_valued_attributes=None)

def mutate(t):
    c = random.randrange(8)
    if c == 0:
        return delete_random_elem(t)
    elif c == 1:
        return add_random_elem(t)
    elif c == 2:
        return replace_random_elem(t)
    elif c == 3:
        return shuffle_random_elem(t)
    elif c == 4:
        return delete_random_attr(t)
    elif c == 5:
        return add_random_attr(t)
    elif c == 6:
        return replace_random_attr(t)
    else:
        return inject_byte(t)
        
def swap_random_elem(t1, t2):
    elem_list1 = get_elem_list(t1)
    elem_list2 = get_elem_list(t2)
    # avoid root swap
    target1 = random.choice([c for c in elem_list1 if c.parent is not None])
    target2 = random.choice([c for c in elem_list2 if c.parent is not None])

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

    return t

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
    c = random.randrange(4)
    if c == 0:
        return swap_random_elem(t)
    elif c == 1:
        return swap_random_attr(t)
    elif c == 2:
        return swap_subtree(t)
    else:
        return swap_attr(t)

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
    test1_soup = bs4.BeautifulSoup(test1, "lxml",multi_valued_attributes=None)
    test2_soup = bs4.BeautifulSoup(test2, "lxml",multi_valued_attributes=None)
    
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