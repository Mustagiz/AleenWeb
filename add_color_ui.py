#!/usr/bin/env python3
with open('Aleen website/admin.html', 'r') as f:
    content = f.read()

# Find the marker for the MRP/discounted price section
idx = content.find('<!-- New MRP and discounted price fields added below -->')
if idx < 0:
    print("Could not find MRP section marker")
    exit(1)

# Color variant management UI to insert
color_ui = """

        <!-- Color Variants Management -->
        <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid rgba(201, 163, 95, 0.2);">
          <label class="form-label" style="font-size: 11px; color: var(--gold-light); display: block; margin-bottom: 6px;">Color Variants</label>
          <div id="colorVariantsContainer">
            <div class="color-variant-row" data-index="0">
              <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px; align-items: center; margin-bottom: 8px;">
                <div>
                  <label class="form-label" style="font-size: 10px; color: #ffffff;">Color Name</label>
                  <input type="text" class="form-control color-name-input" placeholder="e.g. Red, Blue, Green">
                </div>
                <div>
                  <label class="form-label" style="font-size: 10px; color: #ffffff;">Swatch</label>
                  <input type="color" class="form-control swatch-color-input" value="#c9a35f">
                </div>
                <div>
                  <label class="form-label" style="font-size: 10px; color: #ffffff;">Image</label>
                  <input type="file" class="form-control" accept="image/*">
                </div>
                <div>
                  <button type="button" class="btn-remove-color" style="background: transparent; border: none; color: #ff4d4d; font-size: 10px; cursor: pointer;">Remove</button>
                </div>
              </div>
            </div>
          </div>
          <button type="button" class="btn-add-color" style="margin-top: 8px; padding: 6px 12px; background: var(--gold); color: #040906; border: none; border-radius: 4px; font-size: 11px; cursor: pointer;">Add Color Variant</button>
        </div>"""

# Find the position to insert - after the closing of the MRP/discount div
# The marker is at idx, we need to find the end of the section
# Look for the next </div> that closes the form section

# Actually, let me insert right after the MRP/discount section ends
# The section has a specific style div, let me find where it ends

# Find the position after the discount % div
search_from = idx + len('<!-- New MRP and discounted price fields added below -->')
section_end = content.find('</div>', search_from)
if section_end >= 0:
    # There might be multiple </div>, find the right one
    # The MRP section ends with the style div closing
    # Let me just insert after the first </div> from search_from
    insert_pos = section_end + 6  # Include the </div>
    new_content = content[:insert_pos] + color_ui + content[insert_pos:]
    
    with open('Aleen website/admin.html', 'w') as f:
        f.write(new_content)
    print("Added color variant management UI to admin.html")
else:
    print("Could not find section end")