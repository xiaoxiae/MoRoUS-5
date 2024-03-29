from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QSizePolicy
from PyQt5.QtCore import Qt
import codecs
from bisect import bisect_left
import sys


class CorrectMessages(QWidget):
    def __init__(self, *args, **kwargs):
        """Inicializace prvků aplikace."""
        super().__init__(*args, **kwargs)

        # LABEL CREATION
        self.headingLabel = QLabel(self,
            alignment = Qt.AlignCenter,
            text = "<h3>Word Corrector</h3>",
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        # Perecentage of the text corrected
        self.percentageLabel = QLabel(self,
            alignment = Qt.AlignRight,
            toolTip = "Shows the percentage of the sentences corrected.")

        # Words to be corrected
        self.wordLabel = QLabel(self,
            alignment = Qt.AlignCenter,
            wordWrap = True,
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum),
            toolTip = "Displays the sentence with the highlighted word to be corrected.")

        # BUTTON CREATION
        self.startButton = QPushButton(self,
            text = "Start",
            clicked = self.start,
            toolTip = "Starts the correction process.")

        self.includeButton = QPushButton(self,
            text = "Include",
            styleSheet = 'QPushButton {color: green;}',
            enabled=False,
            clicked = self.include,
            toolTip = "Sets the currently highlighted word (and all its future occurences) as correct.")

        self.excludeButton = QPushButton(self,
            text = "Exclude",
            styleSheet = 'QPushButton {color: red;}',
            enabled=False,
            clicked = self.exclude,
            toolTip = "Replaces the word and all of it's future occurences with '-'.")

        self.correctButton = QPushButton(self,
            text = "Adjust",
            styleSheet = 'QPushButton {color: blue;}',
            enabled=False,
            clicked = self.adjust,
            toolTip = "Sets the currently highlighted word (and all its future occurences) to whatever is currently written in the textbox.")

        self.deleteSentenceButton = QPushButton(self,
            text = "Delete sentence",
            styleSheet = 'QPushButton {color: red;}',
            enabled=False,
            clicked = self.deleteCurrentSentence,
            toolTip = "Deletes the sentence that the highlighted word is in. Note that future sentences with this word will NOT be deleted.")

        # Word textbox
        self.textbox = QLineEdit(self,
            returnPressed = self.adjust,
            textChanged = self.textboxTextChanged)

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
        self.mainVLayout.addWidget(self.deleteSentenceButton)

        # Show the main layout
        self.setLayout(self.mainVLayout)
        self.show()


    def textboxTextChanged(self, text):
        """Set correctButton to enabled or disabled based on whether the textbox
        isn't empty."""
        if len(text.strip()) != 0:
            self.correctButton.setEnabled(True)
        else:
            self.correctButton.setEnabled(False)


    def start(self):
        """Starts the entire word correction process."""
        # Disable/enable the appropriate buttons
        self.startButton.setEnabled(False)
        self.includeButton.setEnabled(True)
        self.excludeButton.setEnabled(True)
        self.deleteSentenceButton.setEnabled(True)

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


    def addWordToDictionary(self, word):
        """Adds a word to the czech dictionary."""
        # Find the position of where it should be and add it there
        cz_i = bisect_left(self.cz_dict, word)
        self.cz_dict.insert(cz_i, word)


    def goThroughMessages(self):
        """Goes through the words in the sentence list and stops when it
        reaches one that needs to be corrected."""
        # Go through all of the sentences
        while self.sentenceNumber < len(self.sentences):
            sentence = self.sentences[self.sentenceNumber]

            # Count the percentage of english and czech words in the sentence
            englishWordNumber = 0

            # Go through the words of the sentence
            while self.wordNumber < len(sentence):
                word = sentence[self.wordNumber]

                # Where the word would be inserted into the dictionaries
                cz_i = bisect_left(self.cz_dict, word)
                en_i = bisect_left(self.en_dict, word)

                # If the word has already replaced, skip it
                if word == "-" :
                    self.wordNumber += 1
                    continue

                # If the word is in english, increment the englishWordNumber variable
                if len(self.en_dict) > en_i and self.en_dict[en_i] == word:
                    englishWordNumber += 1

                # If the word isn't in the czech dictionary
                if len(self.cz_dict) <= cz_i or self.cz_dict[cz_i] != word:
                    # If the same correction has already been made, do it again
                    if word in self.corrections:
                        self.sentences[self.sentenceNumber][self.wordNumber] = self.corrections[word]
                        continue

                    # If the word is not czech and is english, set it to "-"
                    if len(self.en_dict) > en_i and self.en_dict[en_i] == word:
                        self.sentences[self.sentenceNumber][self.wordNumber] = "-"
                        continue

                    # Else set the word label accordingly and return
                    self.setWordLabel(word, sentence)

                    # Set the percentage label before returning
                    self.setPercentageLabel()
                    return

                self.wordNumber += 1

            # If a percentage of words are in english, remove the sentence
            if englishWordNumber / len(sentence) > 0.8:
                del(self.sentences[self.sentenceNumber])
            else:
                self.sentenceNumber += 1

            self.wordNumber = 0

        # If everything has been corrected
        self.endOfCorrections()


    def endOfCorrections(self):
        """Is called after the entirety of the text is corrected."""
        # Disables textbox
        self.textbox.setReadOnly(True)
        self.textbox.clear()

        # Disable all buttons
        self.includeButton.setEnabled(False)
        self.excludeButton.setEnabled(False)
        self.correctButton.setEnabled(False)
        self.deleteSentenceButton.setEnabled(False)

        self.wordLabel.setText("<b>Done!</b> All words have been corrected.")
        self.setPercentageLabel()

        # Write the corrected sentences to a file
        output_file = codecs.open("corrected_messages.txt", "w", encoding='utf8')

        for sentence in self.sentences:
            output_file.write(str(" ".join(sentence))+"\n")


    def setWordLabel(self, word, sentence):
        """Set the word label to the current sentence, with the word to be
        corrected highlighted in bold."""

        # Create a copy of the sentence to play around with
        adjustedSentence = list(sentence)

        # Bolden the word that we are correcting
        highlighted_word = "<b>" + adjustedSentence[self.wordNumber] + "</b>"
        adjustedSentence[self.wordNumber] = highlighted_word

        # Adjust the sentence so there is never more than 16 words in total
        maxSentenceLength = 16
        if len(adjustedSentence) <= maxSentenceLength:
            self.wordLabel.setText(' '.join(adjustedSentence))
        else:
            start = self.wordNumber - 8
            end = self.wordNumber + 8

            if start < 0:
                self.wordLabel.setText(' '.join(adjustedSentence[:16]))
            elif end > len(adjustedSentence):
                self.wordLabel.setText(' '.join(adjustedSentence[-16:]))
            else:
                self.wordLabel.setText(' '.join(adjustedSentence[start:end]))


    def setPercentageLabel(self):
        """Sets the percentageLabel to the percentage of the words that
        we've been through."""

        percentage = self.sentenceNumber / len(self.sentences) * 100
        formated_percentage = "{0:.2f}%".format(percentage)

        self.percentageLabel.setText(formated_percentage)


    def include(self):
        """Add the current word to the czech dictionary and run
         goThroughMessages."""

        self.addWordToDictionary(self.sentences[self.sentenceNumber][self.wordNumber])

        self.goThroughMessages()


    def exclude(self):
        """Set the correction of the word to "-" and run goThroughMessages."""

        self.corrections[self.sentences[self.sentenceNumber][self.wordNumber]] = "-"

        self.goThroughMessages()


    def adjust(self):
        """Set the correction of the word to whatever is in the textbox and
        run goThroughMessages."""

        # If there is nothing to adjust, return
        if self.wordLabel.text() == "":
            return

        # Get the word and it's correction
        wordCorrection = self.textbox.text().strip()
        word = self.sentences[self.sentenceNumber][self.wordNumber]

        # If called on an empty textbox, include the word in the dictionary
        if len(wordCorrection) == 0:
            self.include()
            return

        self.textbox.clear()

        # Add the correction to corrections and also to the dictionary
        self.corrections[word] = wordCorrection
        self.addWordToDictionary(wordCorrection)

        self.goThroughMessages()


    def deleteCurrentSentence(self):
        """Deletes the currently selected sentence and runs
        goThroughMessages."""
        del(self.sentences[self.sentenceNumber])

        self.goThroughMessages()


# Run the app
app = QApplication(sys.argv)
correctMessages = CorrectMessages()
app.exec()
