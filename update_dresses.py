#!/usr/bin/env python3
with open('Aleen website/dresses.html', 'r') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if 'grid.innerHTML = items.map(function(item)' in line:
        # Output the new card rendering code
        new_lines.append('  grid.innerHTML = items.map(function(item) {\n')
        new_lines.append('    // Get new fields with fallbacks for backward compatibility\n')
        new_lines.append('    const mrp = item.mrp !== undefined ? Number(item.mrp) : 0;\n')
        new_lines.append('    const discountedPrice = item.discountedPrice !== undefined ? Number(item.discountedPrice) : 0;\n')
        new_lines.append('    const fitLabel = item.fitLabel || "";\n')
        new_lines.append('    const colors = item.garmentColors || [];\n')
        new_lines.append('\n')
        new_lines.append('    // Calculate discount percentage\n')
        new_lines.append('    let discountPercent = 0;\n')
        new_lines.append('    if (mrp > 0 && discountedPrice >= 0) {\n')
        new_lines.append('      discountPercent = Math.round((1 - discountedPrice / mrp) * 100);\n')
        new_lines.append('    }\n')
        new_lines.append('    \n')
        new_lines.append('    // Build color swatches HTML\n')
        new_lines.append('    const colorSwatches = colors.map((c, idx) => {\n')
        new_lines.append('      const swatchColor = c.swatchColor || "#c9a35f";\n')
        new_lines.append('      const img = c.garmentImage ? "/assets/" + c.garmentImage : item.image;\n')
        new_lines.append('      return "<div class=\\"color-swatch\\" data-index=\"" + idx + "\" style=\"background: " + swatchColor + "; width: 24px; height: 24px; border: 2px solid transparent; border-radius: 50%; cursor: pointer; margin-right: 4px;\" title=\"Variant " + (idx + 1) + "\"></div>";\n')
        new_lines.append('    }).join("");\n')
        new_lines.append('\n')
        new_lines.append('    // Build fit tag HTML\n')
        new_lines.append('    const fitTag = fitLabel ? "<span class=\\"fit-tag\\">" + fitLabel + "</span>" : "";\n')
        new_lines.append('\n')
        new_lines.append('    // Build price HTML\n')
        new_lines.append('    const priceHtml = mrp > 0\n')
        new_lines.append('      ? "<span class=\\"card-mrp\\">" + mrp.toLocaleString("en-IN") + "</span>" +')
        new_lines.append('        "<span class=\\"card-discounted-price\\">" + discountedPrice.toLocaleString("en-IN") + "</span>" +')
        new_lines.append('        "<span class=\\"card-discount-percent\\">-" + discountPercent + "%</span>"')
        new_lines.append('      : "<span class=\\"card-price\\">" + Number(item.price).toLocaleString("en-IN") + "</span>";\n')
        new_lines.append('\n')
        new_lines.append('    return "<article class=\\"garment-card\\">" +')
        new_lines.append('      "<div class=\\"card-media\\">" +')
        new_lines.append('        fitTag +')
        new_lines.append('        "<img src=\"" + item.image + "\" alt=\"" + item.title + "\" loading=\"lazy\" />" +')
        new_lines.append('        colorSwatches +')
        new_lines.append('      "</div>" +')
        new_lines.append('      "<div class=\\"card-info\\">" +')
        new_lines.append('        "<span class=\\"card-craft\\">" + (item.craft || "Artisanal") + "</span>" +')
        new_lines.append('        "<h2 class=\\"card-title\\">" + item.title + "</h2>" +')
        new_lines.append('        "<div class=\\"card-prices\\">" + priceHtml + "</div>" +')
        new_lines.append('        "<p class=\\"card-fabric\\">" + (item.fabric || "Pure Silk") + "</p>" +')
        new_lines.append('      "</div>" +')
        new_lines.append('    "</article>";\n')
        new_lines.append('  }).join("");\n')
        # Skip old lines - the old code is about 13 lines
        i += 14
    else:
        new_lines.append(line)
        i += 1

with open('Aleen website/dresses.html', 'w') as f:
    f.writelines(new_lines)

print('dresses.html card rendering updated')