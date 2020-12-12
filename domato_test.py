#!/usr/bin/env python3

from coverage import fitness
from GP.html_seeder import generate_html_tree

with open("domato_sample.html", "r") as f:
    data = f.read()
print(fitness(data))