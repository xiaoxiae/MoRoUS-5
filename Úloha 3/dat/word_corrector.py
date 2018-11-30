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

        # VYTVOŘENÍ OVLÁDACÍCH PRVKŮ
        self.textboxLabel = QLabel(self)
        self.textboxLabel.setAlignment(Qt.AlignCenter)

        self.percentageLabel = QLabel(self)
        self.percentageLabel.setAlignment(Qt.AlignRight)

        self.wordLabel = QLabel(self)
        self.wordLabel.setAlignment(Qt.AlignCenter)
        self.wordLabel.setWordWrap(True)

        self.startButton = QPushButton(self, text = "Start")
        self.startButton.clicked.connect(self.start)

        self.includeButton = QPushButton(self, text = "Include", styleSheet = 'QPushButton {color: green;}', enabled=False)
        self.includeButton.clicked.connect(self.include)
        self.excludeButton = QPushButton(self, text = "Exclude", styleSheet = 'QPushButton {color: red;}', enabled=False)
        self.excludeButton.clicked.connect(self.exclude)
        self.correctButton = QPushButton(self, text = "Adjust", styleSheet = 'QPushButton {color: blue;}', enabled=False)
        self.correctButton.clicked.connect(self.adjust)

        self.textbox = QLineEdit(self)
        self.textbox.returnPressed.connect(self.correctButton.click)

        # ROZLOŽENÍ OVLÁDACÍCH PRVKŮ
        self.layout = QVBoxLayout(self)

        self.labelHLayout = QHBoxLayout(self)
        self.labelHLayout.addWidget(self.textboxLabel)
        self.labelHLayout.addWidget(self.percentageLabel)
        self.textboxLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.textboxLabel.setText("<h3>Word Corrector</h3>")
        self.layout.addLayout(self.labelHLayout)

        # Layout for the textbox and start button
        self.mainHLayout = QHBoxLayout(self)
        self.mainHLayout.addWidget(self.textbox)
        self.mainHLayout.addWidget(self.startButton)
        self.layout.addLayout(self.mainHLayout)

        # Layout for the words to be corrected
        self.layout.addWidget(self.wordLabel)
        self.wordLabel.setText("Press <b>Start</b> to begin.")
        self.wordLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Layout for the buttons
        self.buttonHLayout = QHBoxLayout(self)
        self.buttonHLayout.addWidget(self.includeButton)
        self.buttonHLayout.addWidget(self.excludeButton)
        self.buttonHLayout.addWidget(self.correctButton)
        self.layout.addLayout(self.buttonHLayout)

        # Zobrazení
        self.setLayout(self.layout)
        self.show()

    def start(self):
        # Disable/enable the appropriate buttons
        self.startButton.setEnabled(False)
        self.correctButton.setEnabled(True)
        self.includeButton.setEnabled(True)
        self.excludeButton.setEnabled(True)

        # Load the Czech dictionary
        cz_dict_file = codecs.open("dictionaries/czech.dic", "r", encoding="utf-8")
        self.cz_dict = cz_dict_file.read().splitlines()

        # Load the English dictionary
        en_dict_file = open("dictionaries/english.dic", "r")
        self.en_dict = en_dict_file.read().splitlines()

        # Load the messages file and split each of the messages into words
        words_file = codecs.open("messages.txt", "r", encoding="utf-8")
        messages = words_file.read().splitlines()
        self.sentences = [sentence.split(" ") for sentence in messages]

        # A dictionary to store corrections
        self.corrections = {}

        # Start going through the messages
        self.sentenceNumber = 0
        self.wordNumber = 0

        self.setPercentageLabel()
        self.goThroughMessages()

    def goThroughMessages(self):
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
                    return

                self.wordNumber += 1

            self.wordNumber = 0
            self.sentenceNumber += 1

            self.setPercentageLabel()

    def setWordLabel(self, word, sentence):
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
        # The percentage of the words that we've been through
        percentage = "{0:.2f}%".format(self.sentenceNumber / len(self.sentences) * 100)

        self.percentageLabel.setText(percentage)

    def include(self):
        word = self.sentences[self.sentenceNumber][self.wordNumber]

        # Find the position of where it should be and add it to the dictionary
        cz_i = bisect_left(self.cz_dict, word)
        self.cz_dict.insert(cz_i, word)

        self.goThroughMessages()

    def exclude(self):
        # Set the word (and it's correction) to - (like it's not there)
        self.corrections[self.sentences[self.sentenceNumber][self.wordNumber]] = "-"

        self.goThroughMessages()

    def adjust(self):
        # Get the word and it's correction
        wordCorrection = self.textbox.text()
        word = self.sentences[self.sentenceNumber][self.wordNumber]

        # If the person pressed enter on a correct word, simply include it
        if len(wordCorrection) == 0:
            self.include()
            return

        # Add the correction for the future
        self.corrections[word] = wordCorrection

        self.textbox.clear()

        self.goThroughMessages()

# Spuštění celého programu
app = QApplication(sys.argv)
ordCorrector = WordCorrector()
app.exec()
