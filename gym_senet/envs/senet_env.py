import gym
from typing import Optional
from gym.spaces import Tuple, Discrete, MultiBinary, MultiDiscrete
from gym_senet.envs.senet import Senet
from gym_senet.envs.renderer import HumanRenderer, RgbRenderer, AnsiRenderer


class SenetEnv(gym.Env):

    metadata = {'render_modes': ['human', 'rgb_array', 'ansi'], 'render_fps': 1}

    def __init__(self, num_pieces=5, render_mode=None):

        if render_mode is None:
            self.renderer = None
        elif render_mode == 'human':
            self.renderer = HumanRenderer()
        elif render_mode == 'rgb_array':
            self.renderer = RgbRenderer()
        elif render_mode == 'ansi':
            self.renderer = AnsiRenderer()
        else:
            raise NotImplementedError(f'render mode {render_mode} is not implemented')

        self.senet = Senet(num_pieces=num_pieces)
        self.observation_space = Tuple((MultiBinary([2, Senet.BOARD_SIZE]), Discrete(2)))
        # first component: 0, ..., 29 = Senet.BOARD_SIZE - 1 for regular moves
        # and 30 = Senet.BOARD_SIZE for pass the turn to the opponent
        # second component: 1, 2, 3, 4, 5 for regular moves and 0 for pass the turn
        self.action_space = MultiDiscrete([Senet.BOARD_SIZE + 1, 6])

        self.player = None

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        self.senet.reset()

        self.player = Senet.CONS_PLAYER
        return self.state(), {'legal_actions_fn': self.senet.legal_moves}

    def step(self, action):
        """
        :param action: pair (house of depart, num_steps), when house of depart is Senet.BOARD_SIZE = 30,
                     this is dumb action showing that no legals moves available and the move passes to another player
        :return:
        """

        _, player_wins, pass_turn = self.senet.apply_move(self.player, action)

        done = player_wins
        if player_wins:
            reward = 1 if self.player == Senet.CONS_PLAYER else -1
            info = {'winner': self.player}
        else:
            reward = 0
            if pass_turn:
                self.player = 1 - self.player
            info = {'legal_actions_fn': self.senet.legal_moves}

        # do not use truncation
        return self.state(), reward, done, False, info

    def state(self):
        return self.senet.board, self.player

    def render(self):
        if self.renderer:
            return self.renderer.render(self.senet.board)

    def close(self):
        if self.renderer:
            self.renderer.close()
