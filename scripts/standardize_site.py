import re
import json

with open('Aleen-react2/public/mahira.html', 'r', encoding='utf-8') as f:
    mahira = f.read()

# Extract ALEEN_LOGO JSON
m = re.search(r'window\.ALEEN_LOGO\s*=\s*(\{.*?\});', mahira, re.DOTALL)
if not m:
    raise Exception("ALEEN_LOGO not found")
D = json.loads(m.group(1))

EC = D['center']
ornaments = D['orn']['ne'] + D['orn']['nw'] + D['orn']['se'] + D['orn']['sw']

svg_parts = []
svg_parts.append('<svg id="brandLogo" viewBox="0 0 1600 1351" role="img" aria-label="Aleen Clothing">')
svg_parts.append('''<defs>
  <linearGradient id="lgGold" gradientUnits="userSpaceOnUse" x1="436.7" y1="105.6" x2="1165.3" y2="834.2">
    <stop offset="0%" stop-color="#8a6420"/>
    <stop offset="32%" stop-color="#c9a35f"/>
    <stop offset="50%" stop-color="#f0d48c"/>
    <stop offset="68%" stop-color="#c9a35f"/>
    <stop offset="100%" stop-color="#7c5a1d"/>
  </linearGradient>
  <linearGradient id="lgWmGold" gradientUnits="userSpaceOnUse" x1="0" y1="1000" x2="1600" y2="1180">
    <stop offset="0%" stop-color="#9a7226"/>
    <stop offset="30%" stop-color="#d9b269"/>
    <stop offset="50%" stop-color="#f2d896"/>
    <stop offset="70%" stop-color="#d9b269"/>
    <stop offset="100%" stop-color="#9a7226"/>
  </linearGradient>
  <linearGradient id="lgSelGold" gradientUnits="userSpaceOnUse" x1="280" y1="0" x2="1320" y2="0">
    <stop offset="0%" stop-color="#8a6420"/>
    <stop offset="45%" stop-color="#e7c87f"/>
    <stop offset="60%" stop-color="#f0d48c"/>
    <stop offset="100%" stop-color="#8a6420"/>
  </linearGradient>
</defs>''')

svg_parts.append('<g id="lgAll">')
svg_parts.append('<g id="lgEmblem">')
svg_parts.append(f'<circle id="lgRing" cx="{EC["x"]}" cy="{EC["y"]}" r="{D["ring"]["r"]}" fill="none" stroke="url(#lgGold)" stroke-width="{D["ring"]["w"] + 1}"/>')
svg_parts.append(f'<path id="lgMFill" d="{D["m"]["d"]}" fill="url(#lgGold)" fill-rule="evenodd"/>')

svg_parts.append('<g id="lgDia">')
for k in ['n', 's', 'e', 'w']:
    if k in D['diamonds']:
        svg_parts.append(f'<path d="{D["diamonds"][k]["d"]}" fill="url(#lgGold)" fill-rule="evenodd" class="lg-dia lg-dia-{k}"/>')
svg_parts.append('</g>')

svg_parts.append('<g id="lgOrn">')
for o in ornaments:
    svg_parts.append(f'<path d="{o["d"]}" fill="url(#lgGold)" fill-rule="evenodd" class="lg-orn"/>')
svg_parts.append('</g>')
svg_parts.append('</g>')

svg_parts.append('<g id="lgMah">')
for l in D['mahira']:
    svg_parts.append(f'<path d="{l["d"]}" fill="url(#lgWmGold)" fill-rule="evenodd" class="lg-mah"/>')
svg_parts.append('</g>')

svg_parts.append('''<g id="lgSel">
  <text x="801" y="1318" text-anchor="middle" fill="url(#lgSelGold)" class="lg-sel" style="font-family: 'Great Vibes', cursive, 'Playfair Display', serif; font-size: 155px; font-weight: 400; letter-spacing: 2px;">Consciously Curated</text>
  <rect x="40" y="1300" width="220" height="4" fill="url(#lgSelGold)" class="lg-line lg-line-0"/>
  <rect x="1340" y="1300" width="220" height="4" fill="url(#lgSelGold)" class="lg-line lg-line-1"/>
</g>''')

svg_parts.append('</g></svg>')

STATIC_BRAND_LOGO_SVG = ''.join(svg_parts)

print("STATIC_BRAND_LOGO_SVG generated, length:", len(STATIC_BRAND_LOGO_SVG))
