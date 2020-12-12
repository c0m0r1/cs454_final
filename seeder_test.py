#!/usr/bin/env python3

from coverage import fitness
from GP.html_seeder import generate_html_tree

print(fitness(str(generate_html_tree(7, 7, 2, 2, 5))))