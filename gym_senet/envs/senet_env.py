import gym
from typing import Optional
from gym.spaces import MultiBinary, MultiDiscrete
from gym_senet.envs.senet import Senet
from gym_senet.envs.renderer import BoardRenderer, AnsiRenderer


class SenetEnv(gym.Env):

    metadata = {'render_modes': ['human', 'ansi'], 'render_fps': 1}

    def __init__(self, num_pieces=5, render_mode='human'):

        if render_mode is None:
            self.renderer = None
        elif render_mode == 'human':
            self.renderer = BoardRenderer()
        elif render_mode == 'ansi':
            self.renderer = AnsiRenderer()
        else:
            raise NotImplementedError(f'render mode {render_mode} is not implemented')

        self.senet = Senet(num_pieces=num_pieces)
        self.observation_space = MultiBinary([2, Senet.BOARD_SIZE])
        # first component: 0, ..., 29 = Senet.BOARD_SIZE - 1 for regular moves
        # and 30 = Senet.BOARD_SIZE for pass the turn to the opponent
        # second component: 1, 2, 3, 4, 5 for regular moves and 0 for pass the turn
        self.action_space = MultiDiscrete([Senet.BOARD_SIZE + 1, 6])

        self.player = None

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        self.senet.reset()

        self.player = Senet.CONS_PLAYER
        sticks = self.senet.throw_sticks()
        legal_actions = self.legal_actions(sticks)
        return self.state(), {'player': self.player, 'legal_actions': legal_actions, 'sticks': sticks}

    def legal_actions(self, sticks):
        actions = self.senet.legal_moves(self.player, sticks)
        if not actions:
            # pass turn to another player
            actions = [(Senet.BOARD_SIZE, 0)]
        return actions

    def step(self, action):
        """
        :param action: pair (house of depart, num_steps), when house of depart is Senet.BOARD_SIZE = 30,
                       this is dumb action showing that no legals moves available
        :return:
        """

        if action[0] == Senet.BOARD_SIZE:

            done = False
            reward = 0

            self.player = 1 - self.player
            sticks = self.senet.throw_sticks()
            legal_actions = self.legal_actions(sticks)
            info = {'player': self.player, 'legal_actions': legal_actions, 'sticks': sticks}
        else:

            _, player_wins, pass_turn = self.senet.apply_move(self.player, action)

            done = player_wins
            if player_wins:
                reward = 1 if self.player == Senet.CONS_PLAYER else -1
                info = {'winner': self.player}
            else:
                reward = 0
                if pass_turn:
                    self.player = 1 - self.player
                sticks = self.senet.throw_sticks()
                legal_actions = self.legal_actions(sticks)
                info = {'player': self.player, 'legal_actions': legal_actions, 'sticks': sticks}

        # do not use truncation
        return self.state(), reward, done, False, info

    def state(self):
        # TODO use cache for previous board values, also one channel for player and one channel per each stick
        # should we also add actions? https://github.com/werner-duvaud/muzero-general
        return self.senet.board

    def render(self):
        if self.renderer:
            return self.renderer.render(self.senet.board)

    def close(self):
        if self.renderer:
            self.renderer.close()
