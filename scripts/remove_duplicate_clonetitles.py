#!/usr/bin/env python3
"""
Remove duplicate clonetitle paragraphs while preserving document body.
Rules:
- A clonetitle is a line starting with '<p style="color:gray'.
- If a clonetitle is immediately followed (ignoring blank lines) by a heading line starting with '## '
  and that exact heading has been seen previously in the document, remove the clonetitle line only.
- Also collapse consecutive identical clonetitle lines if they appear back-to-back.
"""
from pathlib import Path

p = Path('PSiCC2-Intro_First_Chapter (rus).md')
s = p.read_text(encoding='utf-8')
lines = s.splitlines()

seen_headings = set()
out_lines = []
i = 0
n = len(lines)
removed = 0

while i < n:
    line = lines[i]
    if line.startswith('<p style="color:gray'):
        # collapse consecutive identical clonetitles
        j = i+1
        while j < n and lines[j] == line:
            j += 1
        if j > i+1:
            # skip duplicates, keep single
            out_lines.append(line)
            removed += (j - (i+1))
            i = j
            continue
        # find next non-empty line
        k = i+1
        while k < n and lines[k].strip() == '':
            k += 1
        next_line = lines[k] if k < n else ''
        if next_line.startswith('## '):
            heading = next_line.strip()
            if heading in seen_headings:
                # remove this clonetitle only
                removed += 1
                i += 1
                continue
            else:
                # keep clonetitle and record heading when the heading is written
                out_lines.append(line)
                i += 1
                continue
        else:
            # keep clonetitle
            out_lines.append(line)
            i += 1
            continue
    else:
        # if this is a heading, record it
        if line.startswith('## '):
            seen_headings.add(line.strip())
        out_lines.append(line)
        i += 1

if removed:
    p.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')
    print(f'Removed {removed} duplicate clonetitle line(s).')
else:
    print('No duplicate clonetitle lines removed.')
