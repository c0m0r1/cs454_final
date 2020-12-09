from coverage import fitness
import os
import random
import string

length_range = (10, 1000)

def primitive_random(iter_cnt):
    max_f = 0
    result = None
    for _ in range(iter_cnt):
        length = random.randint(length_range[0], length_range[1])
        tmp_result = ''.join(random.choice(string.printable) for _ in range(length))
        new_f = fitness(tmp_result)
        if new_f > max_f:
            max_f = new_f
            result = tmp_result 
    return (max_f, result)
    
if __name__ == "__main__":
    print(primitive_random(100))