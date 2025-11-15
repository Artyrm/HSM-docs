#!/usr/bin/env python3
import re
from pathlib import Path
p = Path('PSiCC2-Intro_First_Chapter (rus).md')
s = p.read_text(encoding='utf-8')
# fix nested <p> like <p...>5 <p...>5 (xxxi) Введение</p></p>
s = re.sub(r"(<p[^>]*>)(\d+)\s*<p([^>]*)>(.*?)</p></p>", lambda m: f"{m.group(1)}{m.group(2)} {m.group(4)}</p>", s)
# move markdown headings out of clonetitle lines: <p...>8 # ГЛАВА 1</p> -> <p...>8</p>\n\n# ГЛАВА 1
s = re.sub(r"(<p[^>]*>)(\d+)\s+#\s*(.+?)</p>", lambda m: f"{m.group(1)}{m.group(2)}</p>\n\n# {m.group(3)}", s)
# remove duplicated adjacent identical clonetitle lines
lines = s.splitlines()
out = []
prev = None
for line in lines:
    if line == prev:
        # skip duplicate
        continue
    out.append(line)
    prev = line
s = '\n'.join(out) + '\n'
# remove accidental repeated blocks like the duplicated '9 (4) Глава 1' repeated; remove duplicate paragraphs if identical and within 5 lines
pattern = re.compile(r'(?:\n)(<p[^>]+>.*?</p>\n\n)(?:\1)+', re.S)
# collapse repeats
s = pattern.sub(r'\n\1', s)

p.write_text(s, encoding='utf-8')
print('Cleanup done')
