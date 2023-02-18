import gym
from typing import Optional
from gym.spaces import Tuple, Discrete, MultiBinary, MultiDiscrete
from gym_senet.envs.senet import Senet, SenetGame
from gym_senet.envs.renderer import HumanRenderer, RgbRenderer, AnsiRenderer


class SenetEnv(gym.Env):

    metadata = {'render_modes': ['human', 'rgb_array', 'ansi'], 'render_fps': 1}

    def __init__(self, num_pieces=5, render_mode=None, rules='kendall'):

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

        self.game = SenetGame(num_pieces=num_pieces, rules=rules)
        self.observation_space = Tuple((MultiBinary([2, Senet.BOARD_SIZE]), Discrete(2)))
        self.action_space = Discrete(10 * num_pieces + 1)

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        return self.game.reset(), {'rules': self.game.rules}

    def step(self, action):
        """
        :param action: pair (house of depart, num_steps), when house of depart is Senet.BOARD_SIZE = 30,
                     this is dumb action showing that no legals moves available and the move passes to another player
        :return:
        """

        board, player, reward, done, pass_turn = self.game.apply_move(action)
        info = {'winner': player} if done else {'pass': pass_turn}

        # do not use truncation
        return (board, player), reward, done, False, info

    def render(self):
        if self.renderer:
            return self.renderer.render(self.game.board)

    def close(self):
        if self.renderer:
            self.renderer.close()
