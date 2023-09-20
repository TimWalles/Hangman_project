import os
import random
import shutil
import time
from getpass import getpass

from random_words import RandomWords
from textblob import Word

from tools.hangman.drawn_hangman import drawn_hangman


class Hangman:
    welcome_text = 'Welcome to the Hangman game!'.center(shutil.get_terminal_size().columns)
    introduction_text = '''\nA game where you’ll experience the thrill of life and death decisions! You’ll be guessing letters to save a life, but be warned, one wrong guess and you’ll be responsible for the demise of our stick figure friend. So, choose wisely and try not to let your conscience haunt you as you play this twisted game of fate!'''
    random_words_gen = RandomWords()

    def __init__(self):
        self.first_run = True
        self.initialization_failed = False

    @staticmethod
    def clearTerminal():
        os.system('clear')

    # region class initialization
    def printWelcomeText(self):
        print(self.welcome_text)
        time.sleep(1)
        for word in self.introduction_text.split(' '):
            print(word, flush=True, end=' ')
            time.sleep(0.2)
        print('\n')

    def countdownInitialization(self):
        print('\n')
        for i in ['build a gallows', 'find a volunteer', 'fit the noose        ']:
            print(f'Starting Hangman: {i}\r', flush=True, end='')
            time.sleep(1.5)
        print('\n')

    def setSecretWord(self) -> str:
        secret_word = getpass('Enter secret word or hit [ENTER] for random word to start:').upper()
        if not secret_word:
            secret_word = self.getRandomSecretWord()
        return secret_word

    def setDifficultyLevel(self) -> tuple[float, int]:
        selected_difficulty = input('Select difficulty level\n1. Easy\n2. Medium\n3. Hard\nSelected difficulty:')
        match selected_difficulty:
            case '1':
                return 0.8, 6
            case '2':
                return 0.7, 5
            case '3':
                return 0.6, 4
            case _:
                return float(), int()

    def setAttempts(self, selected_difficulty: float, min_attempts: int) -> float:
        nr_unique_char = len(set(self.secret_word))
        nr_attempts = round(nr_unique_char * selected_difficulty)
        if nr_attempts <= min_attempts:
            return float(min_attempts)
        return nr_attempts

    def initializeHangman(self) -> bool:
        self.clearTerminal()
        self.picked_letter = ''
        self.picked_letters = []
        self.guess_result = ''
        if self.first_run:
            self.printWelcomeText()
            self.first_run = False
        if self.initialization_failed:
            print('\rHangman initialization failed, please check the spelling or try selecting a different secret word...\n')
            self.initialization_failed = False
        secret_word = self.setSecretWord()
        selected_difficulty, min_attempts = self.setDifficultyLevel()
        if all(
            [
                self.inputIsAlphabetic(secret_word),
                self.inputSpelledCorrect(secret_word),
                self.inputIsNotEmpty(secret_word),
                not self.letterIsSingle(secret_word),
                selected_difficulty,
            ]
        ):
            self.secret_word = secret_word
            self.hidden_word = '-' * len(self.secret_word)
            self.remaining_attempts = self.setAttempts(selected_difficulty, min_attempts)
            self.attempt_steps = 6.0 / self.remaining_attempts
            self.countdownInitialization()
            return True
        else:
            self.initialization_failed = True
            return False

    # endregion

    # region validate input
    @staticmethod
    def inputSpelledCorrect(input_string: str) -> bool:
        spellcheck = Word(input_string.lower()).spellcheck()[0]
        return spellcheck[1] >= 0.7 and spellcheck[0].upper() == input_string

    @staticmethod
    def inputIsAlphabetic(input_string: str) -> bool:
        return input_string.isalpha()

    @staticmethod
    def inputIsNotEmpty(input_string: str) -> bool:
        return input_string != ''

    @staticmethod
    def letterIsSingle(input_string: str) -> bool:
        return len(input_string) == 1

    def letterIsNotSelected(self, input_string: str) -> bool:
        return not input_string in self.picked_letters

    def isValidLetter(self, input_string: str) -> bool:
        return all(
            [
                self.inputIsNotEmpty(input_string),
                self.inputIsAlphabetic(input_string),
                self.letterIsSingle(input_string),
                self.letterIsNotSelected(input_string),
            ]
        )

    # endregion

    # region secret word handling
    def getRandomSecretWord(self) -> str:
        list_of_words = self.random_words_gen.random_words(count=20, min_letter_count=10)
        return random.choice(list_of_words).upper()

    def inputInHiddenWord(self) -> bool:
        return self.picked_letter in self.secret_word

    def getLetterIndices(self) -> list[int]:
        return [idx for idx, char in enumerate(self.secret_word) if char == self.picked_letter]

    def updateHiddenWord(self):
        for index in self.getLetterIndices():
            self.hidden_word = self.hidden_word[:index] + self.picked_letter + self.hidden_word[index + 1 :]

    def hiddenWordGuessed(self):
        return self.hidden_word == self.secret_word

    # endregion

    # region game tracking
    def updateAttempts(self):
        self.remaining_attempts -= 1

    def getAttempts(self) -> int:
        return int(self.remaining_attempts)

    def updatePickedLetters(self, picked_letter: str):
        self.picked_letters.append(picked_letter)

    def getPickedLetters(self) -> str:
        return ','.join(self.picked_letters)

    # endregion

    # region game
    def setInputLetter(self, picked_letter):
        self.picked_letter = picked_letter

    def resetInputLetter(self):
        self.picked_letter = ''

    def makeGuess(self, picked_letter: str):
        if self.isValidLetter(picked_letter):
            self.setInputLetter(picked_letter)
            self.updatePickedLetters(self.picked_letter)
            if self.inputInHiddenWord():
                self.updateHiddenWord()
                self.guess_result = f'CORRECT! The word contains letter: {self.picked_letter}\n'
            else:
                self.updateAttempts()
                self.guess_result = f'WRONG! The word does not contains letter: {self.picked_letter}\n'
            self.resetInputLetter()
        else:
            self.guess_result = 'Input letter is invalid, too long or already picked\n'

    # endregion

    # region draw hangman
    def drawGameTrackers(self):
        print(f'The secret word is: {self.hidden_word} \n')
        print(f'The picked letters: {self.getPickedLetters()} \n')
        print(f'The number of attempts left: {int(self.remaining_attempts)} \n')

    def drawHangman(self):
        print(drawn_hangman[round(6 - self.attempt_steps * self.remaining_attempts)])

    def hangHangman(self):
        for i in range(6):
            self.clearTerminal()
            self.drawGameTrackers()
            if i % 2 == 0:
                print(drawn_hangman[7])
            else:
                print(drawn_hangman[8])
            if self.guess_result:
                print(self.guess_result)
            time.sleep(0.5)

    def drawHangmanUI(self):
        self.clearTerminal()
        self.drawGameTrackers()
        self.drawHangman()
        if self.guess_result:
            print(self.guess_result)

    # endregion
