"""A script for removing all non-.json (and non-.py) files in all
subdirectories of the current directory. Used to clean up unnecessary binary
files from the Facebook data."""
import json
import os

# Find all non-json files (and non-py files)
for path, dirs, files in os.walk('.'):
    for file in files:

        # Remove them
        if not file.endswith('.json') and file.endswith('.py'):
            os.remove(os.path.join(path, file))
