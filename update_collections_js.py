#!/usr/bin/env python3
with open('Aleen website/collections.html', 'r') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Check if this is the card rendering section
    if 'card.innerHTML = ' in line and '`' in line:
        # Output the new card rendering code with grid layout
        new_lines.append('          card.innerHTML = `\\n')
        new_lines.append('        <div class="card-media">\\n')
        new_lines.append('          <span class="fit-tag">' + '${item.fitLabel || ""}' + '</span>\\n')
        new_lines.append('          <img src="' + '${formatImgSrc(item.image)}' + '" alt="' + '${item.title}' + '" loading="lazy" decoding="async" onerror="this.onerror=null;this.src=\'assets/pakistani-kurti-1.jpg\'" />' + '\\n')
        new_lines.append('          ' + '${item.garmentColors && item.garmentColors.length > 0 ? \\'<div class=\"color-swatches\"\\>' + item.garmentColors.slice(0, 3).map((c, idx) => \\'<div class=\"color-swatch\" style=\\\"width: 14px; height: 14px; border: 2px solid transparent; border-radius: 50%; background: \\\" + (c.swatchColor || \\\"#c9a35f\\\") + \\\".\\'></div>\\').join(\\\"\") + \\'</div>\\' : \\'\\'}\\n')
        new_lines.append('          ' + '${item.rating > 0 ? \\'<span class=\\"rating-badge\\" style=\\"display: block;\\">★'.repeat(item.rating) + \\' \\' + item.rating + \\'</span>\\' : \\'\\'}\\n')
        new_lines.append('        </div>\\n')
        new_lines.append('        <div class="card-prices">\\n')
        new_lines.append('          ' + '${item.mrp ? \\'<span class=\\"card-mrp\\">' + item.mrp.toLocaleString(\"en-IN\") + \\'</span>\\' : \\'\\'}\\n')
        new_lines.append('          ' + '${item.discountedPrice ? \\'<span class=\\"card-discounted-price\\">' + item.discountedPrice.toLocaleString(\"en-IN\") + \\'</span>\\' : \\'\\'}\\n')
        new_lines.append('          ' + '${item.mrp > 0 ? \\'<span class=\\"card-discount-percent\\">-' + Math.round((1 - item.discountedPrice / item.mrp) * 100) + \\'%\\'</span>\\' : \\'\\'}\\n')
        new_lines.append('        </div>\\n')
        new_lines.append('        ' + '${item.title ? \\'<div class=\\"garment-name\\">' + item.title + \\'</div>\\' : \\'\\'}\\n')
        new_lines.append('      `;\\n')
        # Skip old lines - the old code is about 30 lines
        i += 35
    else:
        new_lines.append(line)
        i += 1

with open('Aleen website/collections.html', 'w') as f:
    f.writelines(new_lines)

print("Updated collections.html card rendering JavaScript with grid layout")