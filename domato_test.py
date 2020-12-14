#!/usr/bin/env python3

from coverage import fitness, get_coverage_info
import os

def domato_test(dir):
    max_f = float('-inf')
    result = None
    for fname in os.listdir(dir):
        with open(os.path.join(dir,fname), "r") as f:
            data = f.read()

        new_f = fitness(data)

        if new_f > max_f:
            max_f = new_f
            result = data 
    return (max_f, result)
        
if __name__ == "__main__":
    result = domato_test("./domato_samples")
    print(result)
    print(get_coverage_info(result[1]))