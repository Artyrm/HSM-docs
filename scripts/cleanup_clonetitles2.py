#!/usr/bin/env python3
"""
Cleanup clonetitle paragraphs: remove stray '#' characters and collapse adjacent duplicate clonetitles.
"""
import re

inp = 'PSiCC2-Intro_First_Chapter (rus).md'
with open(inp, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
prev_ct = None
for line in lines:
    if line.startswith('<p style="color:gray'):
        # remove any '#' characters from inside the tag content
        # preserve other characters
        new = re.sub(r'#', '', line)
        # collapse multiple spaces
        new = re.sub(r'\s{2,}', ' ', new)
        # normalize spacing after tag start
        # if identical to previous clonetitle, skip
        if new == prev_ct:
            continue
        prev_ct = new
        out.append(new)
    else:
        prev_ct = None
        out.append(line)

with open(inp, 'w', encoding='utf-8') as f:
    f.writelines(out)

print('Cleaned clonetitles (removed # and collapsed duplicates).')
