"""A script for removing all unnecessary Facebook data in all subdirectories
of the 'messages' directory."""
import os

for path, dirs, files in os.walk('messages/'):
    # Find all unnecessary Facebook files
    for file in files:

        if not file.endswith(".json"):
            os.remove(os.path.join(path, file))

    # Remove directories that are empty (after file deletion)
    for dir in dirs:
        if not os.listdir(os.path.join(path, dir)):
            os.rmdir(os.path.join(path, dir))
