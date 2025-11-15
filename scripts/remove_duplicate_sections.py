#!/usr/bin/env python3
"""
Remove duplicated sections: find repeated sections with the same heading and identical body and remove the later duplicates.
Specifically targets Markdown '## ' headings.
"""
from pathlib import Path
import re

p = Path('PSiCC2-Intro_First_Chapter (rus).md')
s = p.read_text(encoding='utf-8')
lines = s.splitlines()

# Find indices of lines that start with '## '
heading_indices = [i for i,l in enumerate(lines) if l.startswith('## ')]

removed = 0
# For each pair of consecutive headings, compare their bodies; if identical and same heading, remove second block
for idx in range(len(heading_indices)-1, 0, -1):
    i = heading_indices[idx]
    j = heading_indices[idx-1]
    heading_i = lines[i].strip()
    heading_j = lines[j].strip()
    if heading_i != heading_j:
        continue
    # get body for heading_j: lines (j+1) .. (next heading or EOF)
    end_j = heading_indices[idx] if idx < len(heading_indices) else len(lines)
    end_i = heading_indices[idx+1] if idx+1 < len(heading_indices) else len(lines)
    body_j = '\n'.join(lines[j+1:end_j]).strip()
    body_i = '\n'.join(lines[i+1:end_i]).strip()
    if body_i == body_j:
        # remove the second block (lines i .. end_i-1)
        del lines[i:end_i]
        removed += 1

if removed:
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Removed {removed} duplicate section(s).')
else:
    print('No duplicate sections found.')
