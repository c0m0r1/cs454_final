# from https://stackoverflow.com/questions/2439374/where-to-find-a-list-of-all-the-possible-html-tags-in-python
# we can use one in domato or DOMpurify instead
# TODO : update if need more tags
TAGS = ["a","abbr","acronym","address","area","b","base","bdo","big","blockquote","body","br","button","caption","cite","code","col","colgroup","dd","del","dfn","div","dl","DOCTYPE","dt","em","fieldset","form","h1","h2","h3","h4","h5","h6","head","html","hr","i","img","input","ins","kbd","label","legend","li","link","map","meta","noscript","object","ol","optgroup","option","p","param","pre","q","samp","script","select","small","span","strong","style","sub","sup","table","tbody","td","textarea","tfoot","th","thead","title","tr","tt","ul","var"]

# but attrs are too tag-aware and type sensative...
# maybe we should use grammer of domato for better result
# for now i use some attrs from https://www.w3schools.com/tags/ref_standardattributes.asp
# TODO : update if need more atrrs
ATTRS = ["accesskey", "class", "contenteditable", "dir", "hidden", "draggable", "lang", "style", "title", "translate"]
