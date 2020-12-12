#!/usr/bin/env python3

import bs4
import random
from .html_constants import TAGS, ATTRS
from .html_utils import rand_str


def generate_html_tree(height, width, attr_cnt, str_minlen, str_maxlen, soup=None):
    if soup is None:
        soup = bs4.BeautifulSoup('<html></html>', "lxml", multi_valued_attributes=None)
        root = soup.html
        width_min = 1  # force nonempty tree at root
    else:
        # string (leaf) node, probability same as other tags
        if random.randint(0, len(TAGS)) == 0:
            return bs4.NavigableString(rand_str(str_minlen, str_maxlen))
        else:
            root_attr = {k: rand_str(str_minlen, str_maxlen) for k in random.sample(ATTRS, random.randint(0, attr_cnt))}
            root = soup.new_tag(random.choice(TAGS), attrs=root_attr)
            width_min = 0
    
    if height > 0:
        for _ in range(random.randint(width_min, width)):
            elem = generate_html_tree(height - 1, width, attr_cnt, str_minlen, str_maxlen, soup)
            root.insert(len(root.contents), elem)

    return root
