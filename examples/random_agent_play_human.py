import gym
import time
from gym_senet.envs.senet import Senet
from gym_senet.agents.random_agent import RandomAgent

env = gym.make('gym_senet:senet-v0', render_mode='human')


if __name__ == '__main__':

    agents = {Senet.CONS_PLAYER: RandomAgent('CONS'), Senet.SPOOLS_PLAYER: RandomAgent('SPOOLS')}

    for _ in range(2):

        obs, info = env.reset()
        legal_actions_fn = info['legal_actions_fn']

        env.render()

        time.sleep(1)

        done = False
        while not done:

            board, player = obs

            # active player
            agent = agents[player]

            # obtain legal actions
            sticks = Senet.throw_sticks()
            legal_actions = legal_actions_fn(player, sticks)

            # choose action
            action = agent.act(board, legal_actions)

            # apply the action
            obs, reward, done, _, info = env.step(action)

            # render the env
            env.render()

            time.sleep(0.2)

    # close the env
    env.close()




