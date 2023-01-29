import random


class RandomAgent:

    def __init__(self, name):
        self.name = name

    def act(self, observations, legal_actions):
        return random.choice(legal_actions)
