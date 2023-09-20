from tools.hangman.hangman import Hangman


def keepPlaying(continue_paying: str) -> bool:
    return 'YES' in continue_paying or continue_paying == 'Y'


game_on = True
game_initialized = False
hangman = Hangman()

while game_on:
    # region initialize Hangman
    while not game_initialized:
        game_initialized = hangman.initializeHangman()
    # endregion

    # region draw UI
    hangman.drawHangmanUI()
    picked_letter = input('Please pick a letter: ').upper()
    hangman.makeGuess(picked_letter)
    # endregion

    # region game tracker
    if hangman.hiddenWordGuessed():
        hangman.drawHangmanUI()
        print('CONGRATULATIONS! You guessed the hidden word!\n')
        game_on = False

    if hangman.getAttempts() <= 0:
        hangman.hangHangman()
        print(f'The secret word was {hangman.secret_word}. You have been HANGED!\n')
        game_on = False
    # endregion

    if not game_on:
        continue_paying = input('Play another game - [Y]es or [N]o?').upper()
        game_on = keepPlaying(continue_paying)
        game_initialized = False
