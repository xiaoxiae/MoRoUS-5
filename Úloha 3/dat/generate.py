"""A script to generate words from facebook JSON files (with restrictions)."""
import json
import os
import re
from datetime import datetime
import json
import codecs

# Name of the person to parse the messages of
name = "Tomáš Sláma"

# The latest accepted message date
latest_date = datetime.strptime('Jan 1 2017', '%b %d %Y')

# Regexes to split text into words and to find unwanted text
word_split_regex = re.compile("[^a-zA-ZĚŠČŘŽÝÁÍÉÓŇĎŤŮÚěščřžýáíéóňďťůú]+")
url_regex = "((http|ftp|https):\/\/)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}([-a-zA-Z0-9@:%_\+.~#?&\/=]*)"
email_regex = "[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}"

# Filter applied on each of the words (the "d" and "p" are ":P" and ":D")
word_filter = lambda word: len(word) != 0 and word != "p" and word != "d"

# Create a file to write to
output_file = codecs.open("messages.txt", "w", encoding='utf8')

# Find all non-json files (and non-py files) and remove them
for path, dirs, files in os.walk('.'):
    for input_file in files:

        if input_file.endswith('.json'):
            file_path = os.path.join(path, input_file)

            # Read the json file
            with open(file_path) as input_file:
                data = json.load(input_file)

                # Go through each message
                for message in data["messages"]:

                    # Ignore stickers or photos
                    if "sticker" in message or "photos" in message:
                        continue

                    # Attempt to read all of the parts of the message
                    try:
                        content = message["content"].encode('latin_1').decode('utf-8')
                        sender_name = message["sender_name"].encode('latin_1').decode('utf-8')
                        message_date = datetime.fromtimestamp(message["timestamp_ms"] / 1000)

                        # Skip content contains a link or an email adress
                        if re.search(url_regex, content) or re.search(email_regex, content):
                            continue

                        # If the name and date are correct
                        if sender_name == name and message_date > latest_date:
                            # Split each of the words, filter them and write them to file
                            words = [word.lower() for word in word_split_regex.split(content)]
                            filtered_words = list(filter(word_filter, words))

                            # If there are words to print, print them
                            if len(filtered_words) != 0:
                                output_file.write(str(" ".join(filtered_words))+"\n")
                    except KeyError:
                        pass
