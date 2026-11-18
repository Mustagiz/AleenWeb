#!/bin/sh
cd "$(dirname "$0")"
if ! command -v node >/dev/null 2>&1; then echo "Please install Node.js first."; exit 1; fi
npm install && npm run dev
