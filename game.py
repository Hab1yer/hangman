import re


class HangmanGame:
    def __init__(self, word, difficulty='medium'):
        self._word = word
        self.difficulty = difficulty
        self.guessed = []

    def state(self):
        wrong = [c for c in self.guessed if c not in self._word]
        status = 'won' if set(self._word) <= set(self.guessed) else 'lost' if len(wrong) == 6 else 'playing'
        result = dict(difficulty=self.difficulty, pattern=' '.join(c if c in self.guessed else '_' for c in self._word), guessed_letters=list(self.guessed), incorrect_letters=wrong, remaining_guesses=6-len(wrong), status=status)
        if status != 'playing': result['word'] = self._word
        return result

    def guess(self, letter):
        if self.state()['status'] != 'playing': raise RuntimeError('Game has ended.')
        if not isinstance(letter, str) or not re.fullmatch('[a-zA-Z]', letter): raise ValueError('Enter one English letter.')
        letter = letter.lower()
        if letter in self.guessed: raise RuntimeError('Letter already guessed.')
        self.guessed.append(letter)
