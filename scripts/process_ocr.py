#!/usr/bin/env python3
import re
from pathlib import Path
p = Path('PSiCC2-Intro_First_Chapter (rus).md')
s = p.read_text(encoding='utf-8')

start_re = re.compile(r"==Начало OCR для страницы (\d+)==")
end_re = re.compile(r"==Конец OCR для страницы (\d+)==")

lines = s.splitlines()
out_lines = []
i = 0
N = len(lines)
while i < N:
    m = start_re.match(lines[i])
    if m:
        page = m.group(1)
        # find end marker for same or next separator
        j = i+1
        # collect until matching end marker or next '***' separator
        end_idx = None
        while j < N:
            me = end_re.match(lines[j])
            if me:
                end_idx = j
                break
            if lines[j].strip() == '***':
                # we treat separator as fallback end
                end_idx = j
                break
            j += 1
        if end_idx is None:
            end_idx = j
        # extract content between i+1 and end_idx
        content_block = lines[i+1:end_idx]
        # remove leading blank lines
        k = 0
        while k < len(content_block) and content_block[k].strip() == '':
            k += 1
        content_block = content_block[k:]
        # remove trailing blank lines
        while content_block and content_block[-1].strip() == '':
            content_block.pop()
        # remove isolated state-machine.com lines from content
        content_block = [ln for ln in content_block if ln.strip() != 'state-machine.com']
        # find first non-empty lines
        first = ''
        second = ''
        if content_block:
            first = content_block[0].strip()
        if len(content_block) > 1:
            second = content_block[1].strip()
        # heuristics to form clonetitle
        cl = None
        if first:
            if re.fullmatch(r"\d+", first) and second:
                cl = f"{page} ({first}) {second}"
                # remove first two lines from content
                content_block = content_block[2:]
            else:
                # if first begins with roman or parentheses style like 'xxviii Введение'
                m2 = re.match(r"^(\(?[\w\-\.]+\)?)\s*(.*)$", first)
                if m2:
                    # if first token looks like roman (letters) and rest exists, use parenthesis
                    tok = m2.group(1)
                    rest = m2.group(2)
                    if tok.isalpha() and rest:
                        cl = f"{page} ({tok}) {rest}"
                        # remove first line
                        content_block = content_block[1:]
                    else:
                        # default: use first line as title
                        cl = f"{page} {first}"
                        content_block = content_block[1:]
                else:
                    cl = f"{page} {first}"
                    content_block = content_block[1:]
        else:
            cl = f"{page}"
        # ensure clonetitle is short and trimmed
        cl = cl.strip()
        # write clonetitle as gray paragraph
        out_lines.append(f'<p style="color:gray; margin:0 0 0.5em;">{cl}</p>')
        out_lines.append('')
        # append remaining content block
        out_lines.extend(content_block)
        # if end marker was a '***' we want to keep it
        if end_idx < N and lines[end_idx].strip() == '***':
            out_lines.append('***')
            # skip the separator line
            i = end_idx + 1
        else:
            # end marker consumed, skip it
            i = end_idx + 1
    else:
        # remove isolated 'state-machine.com' outside OCR blocks
        if lines[i].strip() == 'state-machine.com':
            i += 1
            continue
        out_lines.append(lines[i])
        i += 1

new_s = '\n'.join(out_lines) + '\n'
# normalize multiple blank lines (no more than 2)
new_s = re.sub(r'\n{3,}', '\n\n', new_s)

p.write_text(new_s, encoding='utf-8')
print('Processed file written.')
