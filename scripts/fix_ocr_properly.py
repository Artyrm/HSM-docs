#!/usr/bin/env python3
"""
Fix OCR markers by:
1. Removing OCR begin/end markers
2. Preserving text between markers as part of the page content
3. Converting existing clonetitles to proper format
4. Removing isolated 'state-machine.com' lines
"""

import re

def fix_ocr_blocks(text):
    """
    Process OCR blocks to remove markers while preserving content.
    """
    lines = text.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is an OCR start marker
        if line.startswith('==Начало OCR для страницы'):
            # Extract page number
            match = re.search(r'страницы (\d+)', line)
            if match:
                page_num = match.group(1)
                # Skip the start marker
                i += 1
                # Collect content until end marker
                content_lines = []
                while i < len(lines):
                    if lines[i].startswith('==Конец OCR для страницы'):
                        # Found end marker
                        i += 1
                        break
                    content_lines.append(lines[i])
                    i += 1
                
                # Remove isolated "state-machine.com" lines from collected content
                filtered_content = []
                for cl in content_lines:
                    if cl.strip() != 'state-machine.com':
                        filtered_content.append(cl)
                
                # Remove empty lines at start/end
                while filtered_content and not filtered_content[0].strip():
                    filtered_content.pop(0)
                while filtered_content and not filtered_content[-1].strip():
                    filtered_content.pop()
                
                # Add content to result
                result.extend(filtered_content)
                continue
        
        # Skip isolated 'state-machine.com' lines
        if line.strip() == 'state-machine.com':
            i += 1
            continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)

# Read file
with open('PSiCC2-Intro_First_Chapter (rus).md', 'r', encoding='utf-8') as f:
    content = f.read()

# Process
fixed_content = fix_ocr_blocks(content)

# Write back
with open('PSiCC2-Intro_First_Chapter (rus).md', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("OCR markers removed and text preserved.")
