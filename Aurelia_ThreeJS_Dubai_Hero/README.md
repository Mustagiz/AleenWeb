# AURELIA — Genuine Three.js Interactive Dubai Hero

This project replaces the fake zooming background image with a real, navigable 3D architectural environment. All buildings, water, cars, walking figures and helicopter are **Three.js meshes**. The page retains the light Awwwards-inspired design supplied in `DESIGN.md`.

## Recommended: run the developer project

1. Install Node.js 20.19+ (Node 22 also works).
2. Open this folder in VS Code, then open its terminal.
3. Run:

```bash
npm install
npm run dev
```

4. Open the **Local** URL that Vite prints (usually `http://localhost:5173`).
5. To create production files, run `npm run build` and deploy the `dist/` folder to Vercel, Netlify, Cloudflare Pages, or another static host.

## Alternative: no build tools

Open `AURELIA-THREEJS-STANDALONE.html` in Chrome or Edge. This version embeds the CSS and application code. It **still needs an internet connection** to fetch the official Three.js modules from jsDelivr on first load. It uses real 3D, not a static animated image. If local file restrictions block it, use the Vite method above.

## Real 3D controls

- Left-drag / touch-drag: orbit the 3D camera.
- Scroll / pinch: dolly in or out.
- Right-drag: pan.
- Click the highlighted skyscrapers or their floating markers: focus the landmark.
- **DAYLIGHT:** switch between daylight, golden hour, and night materials/lighting.
- **TOUR:** guided camera tour of the major landmarks.
- **FOLLOW HELI:** attach the camera to a genuinely animated 3D helicopter.
- **↺:** reset the camera.
- Cars travel on modeled streets; pedestrians have moving limbs; fountain jets animate.

## Important limitations

This is an **architectural concept model inspired by Downtown Dubai**, not survey-accurate geodata or a licensed photogrammetry capture. Aurelia Tower is a fictional building concept. For photorealistic, geographically accurate buildings, you would need licensed 3D city tiles or commissioned meshes and rights to use them. A real photogrammetry/geospatial integration also typically requires an API key and coverage validation for the exact location.

## Troubleshooting

If the scene is blank, make sure WebGL/hardware acceleration is enabled in Chrome/Edge. Check DevTools Console (F12). If the standalone HTML says its modules cannot load, try the npm/Vite version; it doesn't fetch a 3D library via a CDN at runtime after building. Both versions require WebGL hardware/software support.

This package was syntax-checked but couldn't be browser-render-tested in the creation environment because its npm registry connection was unavailable. Please test on your target device before production deployment.

The enquiry button is only a prototype; it does not send data. Connect it to a back-end or CRM before publishing.
