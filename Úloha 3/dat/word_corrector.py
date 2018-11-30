from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QSizePolicy
from PyQt5.QtCore import Qt
import codecs
from bisect import bisect_left
import sys

# TODO: Add comments to the uncommented methods

class WordCorrector(QWidget):
    def __init__(self, *args, **kwargs):
        """Inicializace prvků aplikace."""
        super().__init__(*args, **kwargs)

        # LABEL CREATION
        self.headingLabel = QLabel(self,
            alignment = Qt.AlignCenter,
            text = "<h3>Word Corrector</h3>",
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))

        # Perecentage of the text corrected
        self.percentageLabel = QLabel(self,
            alignment = Qt.AlignRight)

        # Words to be corrected
        self.wordLabel = QLabel(self,
            text = "Press <b>Start</b> to begin.",
            alignment = Qt.AlignCenter,
            wordWrap = True,
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))

        # BUTTON CREATION
        self.startButton = QPushButton(self,
            text = "Start",
            clicked = self.start)

        self.includeButton = QPushButton(self,
            text = "Include",
            styleSheet = 'QPushButton {color: green;}',
            enabled=False,
            clicked = self.include)

        self.excludeButton = QPushButton(self,
            text = "Exclude",
            styleSheet = 'QPushButton {color: red;}',
            enabled=False,
            clicked = self.exclude)

        self.correctButton = QPushButton(self,
            text = "Adjust",
            styleSheet = 'QPushButton {color: blue;}',
            enabled=False,
            clicked = self.adjust)

        # Word textbox
        self.textbox = QLineEdit(self,
            returnPressed = self.correctButton.click)

        # LAYOUT SETUP
        self.mainVLayout = QVBoxLayout(self)

        # Heading and percentage
        self.labelHLayout = QHBoxLayout(self)
        self.labelHLayout.addWidget(self.headingLabel)
        self.labelHLayout.addWidget(self.percentageLabel)

        # Textbox and startbutton
        self.centerHLayout = QHBoxLayout(self)
        self.centerHLayout.addWidget(self.textbox)
        self.centerHLayout.addWidget(self.startButton)

        # The include, exclude and correct buttons
        self.buttonHLayout = QHBoxLayout(self)
        self.buttonHLayout.addWidget(self.includeButton)
        self.buttonHLayout.addWidget(self.excludeButton)
        self.buttonHLayout.addWidget(self.correctButton)

        # Add all the h-layouts to the main v-layout
        self.mainVLayout.addLayout(self.labelHLayout)
        self.mainVLayout.addLayout(self.centerHLayout)
        self.mainVLayout.addWidget(self.wordLabel)
        self.mainVLayout.addLayout(self.buttonHLayout)

        # Show the main layout
        self.setLayout(self.mainVLayout)
        self.show()


    def start(self):
        # Disable/enable the appropriate buttons
        self.startButton.setEnabled(False)
        self.correctButton.setEnabled(True)
        self.includeButton.setEnabled(True)
        self.excludeButton.setEnabled(True)

        # Load the dictionaries
        cz_dict_file = codecs.open("dictionaries/czech.dic", "r", encoding="utf-8")
        self.cz_dict = cz_dict_file.read().splitlines()

        en_dict_file = open("dictionaries/english.dic", "r")
        self.en_dict = en_dict_file.read().splitlines()

        # Load the messages file and split each of the messages into words
        words_file = codecs.open("messages.txt", "r", encoding="utf-8")
        messages = words_file.read().splitlines()
        self.sentences = [sentence.split(" ") for sentence in messages]

        # A dictionary to store corrections
        self.corrections = {}

        # Variables to track the current word
        self.sentenceNumber = 0
        self.wordNumber = 0

        # Start going through the messages
        self.setPercentageLabel()
        self.goThroughMessages()


    def goThroughMessages(self):
        """Goes through the words in the sentence list and stops when it
        reaches one that needs to be corrected."""
        # Go through all of the sentences
        while self.sentenceNumber < len(self.sentences):
            sentence = self.sentences[self.sentenceNumber]

            # Go through the words of the sentence
            while self.wordNumber < len(sentence):
                word = sentence[self.wordNumber]

                # Where the word would be inserted into the dictionaries
                cz_i = bisect_left(self.cz_dict, word)
                en_i = bisect_left(self.en_dict, word)

                # If the word has already replaced been or is in english, skip it
                if word == "-" :
                    self.wordNumber += 1
                    continue

                # If the word isn't a recognized czech word
                if len(self.cz_dict) <= cz_i or self.cz_dict[cz_i] != word:
                    # If the word english, replace it with "-" and continue
                    if len(self.en_dict) > en_i and self.en_dict[en_i] == word:
                        self.sentences[self.sentenceNumber][self.wordNumber] = "-"
                        continue

                    # If the same correction has already been made, correct it and continue
                    if word in self.corrections:
                        self.sentences[self.sentenceNumber][self.wordNumber] = self.corrections[word]
                        continue

                    # Else set the word label accordingly and return
                    self.setWordLabel(word, sentence)

                    # Set the percentage label before returning
                    self.setPercentageLabel()
                    return

                self.wordNumber += 1

            self.wordNumber = 0
            self.sentenceNumber += 1


    def setWordLabel(self, word, sentence):
        """Set the word label to the current sentence, with the word to be
        corrected highlighted in bold."""

        prettySentence = ""

        # TODO: Fix the shortening of the sentence
        """
        wordLocation = sentence.index(word)
        shortenedSentence = sentence

        # If the sentence is too long, shorten it (to focus on the context of the word)
        if len(sentence) > 16:
            if wordLocation < 8:
                shortenedSentence = sentence[0:16]
            else:
                shortenedSentence = sentence[wordLocation - 8: wordLocation + 8]
        """

        for w in sentence:
            # Highlight our word in the sentence
            if w == word:
                prettySentence += "<b>"+w+"</b> "
            else:
                prettySentence += w + " "

        self.wordLabel.setText(prettySentence.strip())


    def setPercentageLabel(self):
        """Sets the percentageLabel to the percentage of the words that
        we've been through."""

        percentage = self.sentenceNumber / len(self.sentences) * 100
        formated_percentage = "{0:.2f}%".format(percentage)

        self.percentageLabel.setText(formated_percentage)


    def include(self):
        """Add the current word to the czech dictionary and run
         goThroughMessages."""

        word = self.sentences[self.sentenceNumber][self.wordNumber]

        # Find the position of where it should be and add it there
        cz_i = bisect_left(self.cz_dict, word)
        self.cz_dict.insert(cz_i, word)

        self.goThroughMessages()


    def exclude(self):
        """Set the correction of the word to "-" and run goThroughMessages."""

        self.corrections[self.sentences[self.sentenceNumber][self.wordNumber]] = "-"

        self.goThroughMessages()


    def adjust(self):
        """Set the correction of the word to whatever is in the textbox and
        run goThroughMessages."""

        self.textbox.clear()

        # Get the word and it's correction
        wordCorrection = self.textbox.text()
        word = self.sentences[self.sentenceNumber][self.wordNumber]

        # If called on an empty textbox, include the word in the dictionary
        if len(wordCorrection) == 0:
            self.include()
            return

        # Add the correction for the future
        self.corrections[word] = wordCorrection

        self.goThroughMessages()

# Run the app
app = QApplication(sys.argv)
wordCorrector = WordCorrector()
app.exec()
