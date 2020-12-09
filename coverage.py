import json
import subprocess, os
import re
import tempfile
import time

def fitness(test):
    total, covered, cov_li = get_coverage_info(test)
    return covered/total

def get_coverage_info(test):
    runner_template = open('DOMpurify_src/runner_template.js','r').readlines()
    with open("DOMpurify_src/runner.js", "w") as f:
        f.write("dirty = `{}`\n".format(re.escape(test)))
        f.writelines(runner_template)

    result_dir = tempfile.TemporaryDirectory()
        
    result = subprocess.check_output(["c8", "-r", "text-lcov", "-o", result_dir.name, "node", "DOMpurify_src/runner.js"]).decode()
    
    is_purify = False
    coverage_list = []
    curr = -1
    idx = 1

    for l in result.split("\n"):
        if "purify.js" in l:
            is_purify = True
        if not is_purify: continue
        elif "end_of_record" in l: break
        if l[:3] == "DA:":
            line, is_covered = int(l[3:].split(",")[0]), int(l[3:].split(",")[1])
            if is_covered > 0:
                if curr == -1:
                    curr = idx
            elif curr != -1:
                coverage_list.append((curr, idx - 1))
                curr = -1
            idx += 1
        elif l[:3] == "LF:":
            total_line = int(l[3:])
        elif l[:3] == "LH:":
            covered_lien = int(l[3:])
    return (total_line, covered_lien, coverage_list)

if __name__ == "__main__":
    st = time.time()
    total, covered, cov_li = get_coverage_info('<div></div>')
    elapsed = time.time() - st
    print("{:f}% covered".format(covered * 100/total))
    print(cov_li)
    print("elapsed time : {} sec".format(elapsed))