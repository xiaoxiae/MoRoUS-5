from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import re
import codecs

import sys

class Autocomplete(QWidget):
    def __init__(self, *args, **kwargs):
        """Inicializace prvků aplikace."""
        super().__init__(*args, **kwargs)

        # VYTVOŘENÍ OVLÁDACÍCH PRVKŮ
        self.headingLabel = QLabel(self,
            text = "<h3>Autocomplete</h3>",
            alignment = Qt.AlignCenter)

        self.textbox = QLineEdit(self,
            textChanged = self.textboxChanged)

        self.predictionLabel = QLabel(self,
            alignment = Qt.AlignCenter,
            styleSheet = 'color: grey')

        self.fileNameTextbox = QLineEdit(self,
            toolTip = "Input the absolute/relative path to the file to read the data from.")

        self.fileNameButton = QPushButton(self,
            text = "Generate model",
            clicked = self.readFile,
            toolTip = "Loads the data file to the autocomplete model.")

        # ROZLOŽENÍ OVLÁDACÍCH PRVKŮ
        self.layout = QVBoxLayout(self)

        self.fileInputHLayout = QHBoxLayout(self)
        self.fileInputHLayout.addWidget(self.fileNameTextbox)
        self.fileInputHLayout.addWidget(self.fileNameButton)

        self.layout.addWidget(self.headingLabel)
        self.layout.addLayout(self.fileInputHLayout)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.predictionLabel)

        # The number of recommendations to make
        self.rNumber = 5
        self.trieGenerated = False

        # Show the layout
        self.setLayout(self.layout)
        self.show()


    def readFile(self):
        """Starts the trie generation from the specified input file."""
        try:
            self.generateTrie(self.fileNameTextbox.text())
        except FileNotFoundError:
            QMessageBox.about(self, "Error!", "File not found.")

        self.fileNameTextbox.setReadOnly(True)
        self.fileNameTextbox.clear()
        self.fileNameButton.setEnabled(False)

        # Create an "allWords" set that includes all known words from the trie
        list = []
        self.getTrieWords(self.trie, "", list)
        self.allWords = set(word[0] for word in list)

        # To signalize that we can start correcting
        self.trieGenerated = True


    def trieWordValue(self, word):
        """Returns the frequency of the word if the word is in self.trie and
        None if it is not."""
        # Walk the trie until the last word character
        trieBranch = self.trie
        for letter in word[:-1]:
            if letter in trieBranch:
                trieBranch = trieBranch[letter][0]
            else:
                return None

        # If the frequency of the word in the trie isn't 0
        if word[-1] in trieBranch and trieBranch[word[-1]][1] != 0:
            return trieBranch[word[-1]][1]
        else:
            return None


    def generateTrie(self, fileName):
        """Generates a trie from the dat/messages.txt file"""
        self.trie = {}

        with codecs.open(fileName, encoding="UTF-8") as f:
            for sentence in f:

                # Get each of the words of the sentence and iterate over them
                words = sentence.strip().split(" ")
                for i in range(len(words)):
                    word = words[i]

                    if word == "-":
                        continue

                    # Add each of the words to trie
                    self.addWordToTrie(self.trie, word)

                    # If there is a word that follows this one
                    if i < len(words) - 1 and words[i + 1] != "-":
                        followingWord = words[i + 1]

                        # Traverse the till the very last branch
                        trieBranch = self.trie
                        for i in range(len(word)):
                            character = word[i]

                            # Add a new trie with the word that follow this one
                            if i == len(word) - 1:

                                if len(trieBranch[character]) != 3:
                                    trieBranch[character].append({})

                                # Create a new trie with the word
                                self.addWordToTrie(trieBranch[character][2], followingWord)

                            trieBranch = trieBranch[character][0]


    def addWordToTrie(self, trie, word):
        """Adds a word to a trie."""
        trieBranch = trie

        # Go through all the characters of the word
        for i in range(len(word)):
            character = word[i]

            # If this character is not in a trie, add it
            if character not in trieBranch:
                trieBranch[character] = [{}, 0]

            # If we are at the end of the word, increment frequency
            if i == len(word) - 1:
                trieBranch[character][1] += 1

            # Go further into the branch
            trieBranch = trieBranch[character][0]


    def textboxChanged(self, text):
        """Funkce volána s každou změnou textboxu."""
        # If there textbox is empty or the model hasn't been generated
        if len(text) == 0 or not self.trieGenerated:
            self.predictionLabel.setText("")
            return

        # Match the last word
        regex = "\s*([a-zěščřžýáíéóňďťůú]+)$"
        wordSeach = re.search(regex, text.strip())

        # If there is no word, return
        if wordSeach == None:
            return
        word = wordSeach.group(0).strip()

        # If the word is in trie, recommend its connections
        if self.trieWordValue(word):

            # Traverse till we can
            trieBranch = self.trie
            for i in range(len(word)):
                character = word[i]

                # If we're at the last trie branch and the word has connections
                if i == len(word) - 1 and len(trieBranch[character]) == 3:
                    # Get its connections
                    list = []
                    self.getTrieWords(trieBranch[character][2], "", list)

                    # Recommend the top few to the user
                    predictions = sorted(list, key=lambda x:x[1], reverse=True)
                    self.setPredictionLabel(predictions)
                    return

                trieBranch = trieBranch[character][0]

        # Traverse the trie
        trieBranch = self.trie
        for letter in word:
            # Traverse if we can and write possible corrections if we can't
            if letter in trieBranch:
                trieBranch = trieBranch[letter][0]
            else:
                corrections = self.getWordCorrections(word)
                self.setPredictionLabel(corrections)
                return

        # Get all of the possible words from the trie
        predictions = self.getPredictionsFromTrie(trieBranch, word)
        self.setPredictionLabel(predictions)


    def setPredictionLabel(self, predictions):
        """Sets the predictionLabel to the first few predictions."""
        predictionString = "  ".join([w[0] for w in predictions[:self.rNumber]])
        self.predictionLabel.setText(predictionString)


    def getWordCorrections(self, word):
        """Returns possible corrections of a word."""
        # Gets the words that are one edit away and are in the allWords set
        words = [w for w in self.wordEdits(word) if w in self.allWords]

        # Sort them by their values in trie
        sortedWords = sorted([(w, self.trieWordValue(w)) for w in words],
            key=lambda x:x[1])

        return sortedWords


    def wordEdits(self, word):
        """Returns edits that are one away from the word as a set."""

        letters    = 'abcdefghijklmnopqrstuvwxyzěščřžýáíéóňďťůú'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]

        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]

        return set(deletes + transposes + replaces + inserts)


    def getPredictionsFromTrie(self, trie, word):
        """Return words from a trie in a sorted order."""
        list = []
        self.getTrieWords(trie, word, list)
        return sorted(list, key=lambda x:x[1], reverse=True)


    def getTrieWords(self, trie, word, list):
        """Adds the words and their frequencies from the trie to the list."""
        for letter, letterData in trie.items():
            # If the frequency isn't 0, add it to the list
            if letterData[1] != 0:
                list.append((word + letter, letterData[1]))

            # Recursively do the same for the rest of the trie branch
            self.getTrieWords(trie[letter][0], word + letter, list)


# Spuštění celého programu
app = QApplication(sys.argv)
crossing = Autocomplete()
app.exec()
