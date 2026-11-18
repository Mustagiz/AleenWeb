---
version: alpha
name: Awwwards
description: "Light monochrome interface measured from awwwards.com: Inter Tight type, tonal surfaces and 4px corners."
colors:
  background: "#F8F8F8"
  surface: "#F8F8F8"
  on-surface: "#222222"
  on-background: "#222222"
  surface-container-low: "#FFFFFF"
  surface-container: "#EDEDED"
  surface-container-high: "#BDB6A9"
  outline: "#FFFFFF"
  outline-variant: "#A7A7A7"
  primary: "#222222"
  on-primary: "#FFFFFF"
  secondary: "#FFF083"
typography:
  headline-display:
    fontFamily: Inter Tight
    fontSize: 74.5px
    fontWeight: 600
    lineHeight: 1
  headline-lg:
    fontFamily: Inter Tight
    fontSize: 38px
    fontWeight: 300
    lineHeight: 1.3
  body-md:
    fontFamily: Inter Tight
    fontSize: 14px
    fontWeight: 300
    lineHeight: 2
  body-lg:
    fontFamily: Inter Tight
    fontSize: 18px
    fontWeight: 300
    lineHeight: 1.56
  body-sm:
    fontFamily: Inter Tight
    fontSize: 13px
    fontWeight: 300
    lineHeight: 2.15
  label-md:
    fontFamily: Inter Tight
    fontSize: 14px
    fontWeight: 400
    lineHeight: 2
  headline-display-mobile:
    fontFamily: Inter Tight
    fontSize: 36px
    fontWeight: 600
    lineHeight: 1
  headline-lg-mobile:
    fontFamily: Inter Tight
    fontSize: 22px
    fontWeight: 300
    lineHeight: 1.3
rounded:
  sm: 4px
  md: 8px
  lg: 72px
spacing:
  xs: 4px
  sm: 6px
  md: 12px
  lg: 20px
  xl: 37.89px
  gutter: 10px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 0px 20px
    height: 42px
  button-primary-hover:
    backgroundColor: "#383838"
  button-outline:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 0px 15.6px
    height: 60px
  button-ghost:
    textColor: "#DEDEDE"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 0px 12px
    height: 48px
  input-field:
    textColor: "{colors.on-surface}"
    typography: "{typography.body-sm}"
    rounded: 0px
    padding: 0px 0px 0px 38px
  link:
    textColor: "{colors.primary}"
---

# Awwwards Design System

## Overview

Awwwards describes itself as: “Cutting-edge website for a luxury real estate project” The interface is light, built on **Snow (#F8F8F8)** with **Charcoal (#222222)** text and almost no color: actions are carried by contrast, not hue.

Type is set in **Inter Tight**. Headlines run large; body text is 14px. The surface language is flat. Corners are mostly 4px.

Measured from [awwwards.com](https://www.awwwards.com/sites/pyzhevsky) on November 4, 2026 at 1440×900 and 390×844 from 270 rendered elements. Values are computed styles from the live page, not the original source files.

## Colors

The palette has 10 roles.

- **Snow (#F8F8F8):** Page background, seen 4 times. Token `background`, CSS `--bg-primary`.
- **Charcoal (#222222):** Primary text and headings, seen 82 times. Token `on-surface`, CSS `--border-table`.
- **White (#FFFFFF):** Raised areas one step from the page, seen 2 times. Token `surface-container-low`, CSS `--check-toggle-color-ball`.
- **Mist (#EDEDED):** Cards and panels, seen 4 times. Token `surface-container`, CSS `--border-gray`.
- **Light Orange (#BDB6A9):** Hover and pressed fills, seen 1 time. Token `surface-container-high`.
- **White (#FFFFFF):** Borders and dividers, seen 7 times. Token `outline`, CSS `--check-toggle-color-ball`.
- **Gray (#A7A7A7):** Secondary dividers, seen 5 times. Token `outline-variant`.
- **Charcoal (#222222):** Primary buttons and calls to action, seen 141 times. Token `primary`, CSS `--border-table`.
- **White (#FFFFFF):** Text and icons on primary. Token `on-primary`.
- **Light Yellow (#FFF083):** Secondary buttons, seen 3 times. Token `secondary`, CSS `--color-learn`.

## Typography

**Inter Tight** carries the whole interface. Fallback stack: `Inter Tight`.

- **headline-display:** Inter Tight 74.5px at weight 600, line height 1, uppercase (36px on mobile). Page title (h1).
- **headline-lg:** Inter Tight 38px at weight 300, line height 1.3 (22px on mobile). Section headings (h2).
- **body-md:** Inter Tight 14px at weight 300, line height 2. Body text.
- **body-lg:** Inter Tight 18px at weight 300, line height 1.56. Lead paragraphs.
- **body-sm:** Inter Tight 13px at weight 300, line height 2.15. Secondary and small text.
- **label-md:** Inter Tight 14px at weight 400, line height 2. Buttons, navigation and labels.

## Layout

Spacing is mostly on a 4px grid (75% of measured values), with some off-grid steps. Match the measured scale rather than rounding everything.

- **Scale:** xs 4px, sm 6px, md 12px, lg 20px, xl 37.89px.
- **Gaps:** 10px is the most common gap in flex and grid layouts.
- **Breakpoints:** 576px, 700px, 768px, 1000px, 1024px, 1100px, 1168px, 1184px, 1270px, 1280px, 1360px, 1490px, 1556px, 1578px, 1600px, 1780px, 2291px.

## Elevation & Depth

The design is flat: no shadows were measured. Hierarchy comes from tonal surface steps (#FFFFFF → #EDEDED → #BDB6A9) and #FFFFFF borders.

## Shapes

Most elements use 4px corners. Measured radii, most used first:

- **sm (4px):** 32 elements.
- **md (8px):** 32 elements.
- **lg (72px):** 28 elements.

## Components

Measured from the rendered page. Token values reference the tokens above.

- **button-primary (“Be Pro”):** #222222 fill, #FFFFFF text, 14px/500, 8px radius, padding 0px 20px.
- **button-primary-hover:** background #383838, text #FFFFFF on hover.
- **button-outline (“Visit Site”):** #FFF083 fill, #222222 text, 13px/600, 8px radius, padding 0px 15.6px.
- **button-ghost (“Elements”):** transparent fill, #DEDEDE text, 13px/400, 8px radius, padding 0px 12px, border 1px solid #4E4E4E.
- **input-field (“Search by Inspiration”):** transparent fill, #222222 text, 13.3px/400, padding 0px 0px 0px 38px.
- **link:** transparent fill, #222222 text, padding 0px.

## Do's and Don'ts

- Do use #F8F8F8 for the page and lift surfaces in small steps: #FFFFFF, #EDEDED, #BDB6A9.
- Do let contrast carry emphasis; primary actions use #222222 on #F8F8F8.
- Do reuse the measured spacing steps (6px, 12px, 20px).
- Do use 4px corners on most elements; larger surfaces also use 8px and 72px.
- Don't add drop shadows for depth; use tonal surfaces.
- Don't introduce new font families beyond Inter Tight.
- Don't add saturated accent colors; the measured palette is almost entirely neutral.
- Don't make interface transitions slower than 0.3s.

## Motion

Interface transitions are quick: 0.3s.

- **Easing:** `ease`, `ease-in-out`.

Generated by [Sitepeel](https://sitepeel.dev/design-md/awwwards.com/sites/pyzhevsky/), the free DESIGN.md generator (engine 2026.10.29+b828a475ee10).
