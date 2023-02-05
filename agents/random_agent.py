import random


class RandomAgent:

    LEGAL_ACTIONS = 'legal_actions'

    def __init__(self, name):
        self.name = name

    def act(self, **kwargs):
        return random.choice(kwargs[RandomAgent.LEGAL_ACTIONS])
