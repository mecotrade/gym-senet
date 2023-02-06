import random


class RandomAgent:

    LEGAL_ACTIONS = 'legal_actions'

    def __init__(self, name):
        self.name = name

    def act(self, legal_actions, *_):
        return random.choice(legal_actions)
