#!/usr/bin/env python3
# Normalize OCR blocks into single-line clonetitles while preserving body text
import re

inp = 'PSiCC2-Intro_First_Chapter (rus).md'
with open(inp, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
i = 0
n = len(lines)
while i < n:
    line = lines[i]
    if line.startswith('==Начало OCR для страницы'):
        m = re.search(r'страницы\s*(\d+)', line)
        page = m.group(1) if m else ''
        i += 1
        # collect until end
        block = []
        while i < n and not lines[i].startswith('==Конец OCR для страницы'):
            block.append(lines[i].rstrip('\n'))
            i += 1
        # skip end marker if present
        if i < n and lines[i].startswith('==Конец OCR для страницы'):
            i += 1
        # filter out isolated state-machine.com
        block = [b for b in block if b.strip() != 'state-machine.com']
        # remove leading/trailing empty
        while block and not block[0].strip():
            block.pop(0)
        while block and not block[-1].strip():
            block.pop()
        # identify clonetitle pieces
        cl_num = page
        cl_orig = None
        cl_title = None
        body = []
        if block:
            # Find a suitable title line inside the OCR block.
            # Rules:
            # - skip empty lines and isolated 'state-machine.com'
            # - treat a pure number line as original page number (cl_orig)
            # - skip lines that are just chapter headings like 'ГЛАВА 1' (possibly prefixed with '#')
            # - prefer the first substantive line that is not a simple 'ГЛАВА' label or a lone number
            title_idx = None
            for idx, raw in enumerate(block):
                s = raw.strip()
                if not s:
                    continue
                if s == 'state-machine.com':
                    continue
                # skip lines that start with markdown heading markers like '#',
                # because the descriptive clonetitle must not begin with a heading
                if raw.lstrip().startswith('#'):
                    continue
                # pure digits -> original page number
                if cl_orig is None and re.fullmatch(r'\d+', s):
                    cl_orig = s
                    continue
                # strip leading markdown hashes for analysis
                s_nohash = s.lstrip('#').strip()
                # skip terse chapter labels like 'ГЛАВА 1' or 'Глава 1'
                if re.fullmatch(r'(?i)глава\s+\d+', s_nohash):
                    continue
                # skip lines that are just a small roman numeral or lone digit
                if re.fullmatch(r'\(?[ivxlcdmIVXLCDM]+\)?', s_nohash):
                    continue
                if re.fullmatch(r'\d+', s_nohash):
                    continue
                # Accept this line as the title
                cl_title = s_nohash
                title_idx = idx
                break
            # determine body start
            if title_idx is not None:
                body = block[title_idx+1:]
            elif cl_orig is not None:
                # if only original page number found, consume it and keep rest as body
                # find index of cl_orig
                for idx, raw in enumerate(block):
                    if raw.strip() == cl_orig:
                        body = block[idx+1:]
                        break
            else:
                body = block
        # build clonetitle string
        cl_parts = []
        if cl_num:
            cl_parts.append(cl_num)
        if cl_orig:
            cl_parts.append(f'({cl_orig})')
        if cl_title:
            cl_parts.append(cl_title)
        if cl_parts:
            cl_line = '<p style="color:gray; margin:0 0 0.5em;">' + ' '.join(cl_parts) + '</p>'
            # Avoid inserting duplicate clonetitle: check nearby lines (prev 6, next 6)
            def nearby_has_same_clonetitle(out_lines, remaining_lines, candidate):
                # check last up to 6 output lines
                for ln in out_lines[-6:]:
                    if ln.strip() == candidate:
                        return True
                # check next up to 6 remaining source lines
                for rem in remaining_lines[:6]:
                    if rem.strip() == candidate:
                        return True
                return False

            remaining = lines[i:]
            if not nearby_has_same_clonetitle(out, remaining, cl_line):
                out.append(cl_line + '\n')
        # append body lines
        for b in body:
            out.append(b + '\n')
        continue
    else:
        out.append(line)
        i += 1

with open(inp, 'w', encoding='utf-8') as f:
    f.writelines(out)
print('Normalized OCR clonetitles.')
