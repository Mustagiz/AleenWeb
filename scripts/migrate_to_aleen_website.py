import os
import shutil
import re
import json

SOURCE_DIR = os.path.abspath("Aleen-react2/public")
DEST_DIR = os.path.abspath("Aleen website")

os.makedirs(DEST_DIR, exist_ok=True)

print(f"Migrating from {SOURCE_DIR} to {DEST_DIR}...")
