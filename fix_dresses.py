#!/usr/bin/env python3
with open('Aleen website/dresses.html', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    # Check if this is the start of the old leftover pattern (after line 2365)
    if i > 2365 and "      '</div>' +" in line:
        skip = True
        continue
    elif skip:
        # Skip this line and the next if it contains the old join pattern
        if "  ").join('');" in line:
            skip = False
            continue
        else:
            continue
    else:
        new_lines.append(line)

with open('Aleen website/dresses.html', 'w') as f:
    f.writelines(new_lines)

print("Fixed dresses.html duplicate code")