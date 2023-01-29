import gym
import time
from gym_senet.envs.senet import Senet
from examples.agents import RandomAgent

env = gym.make('gym_senet:senet-v0', render_mode='human')


if __name__ == '__main__':

    agents = {Senet.CONS_PLAYER: RandomAgent('CONS'), Senet.SPOOLS_PLAYER: RandomAgent('SPOOLS')}

    for _ in range(2):

        obs, info = env.reset()

        env.render()

        time.sleep(1)

        done = False
        while not done:

            # active player
            agent = agents[info['player']]

            # obtain legal actions
            legal_actions = info['legal_actions']

            # choose action
            action = agent.act(obs, legal_actions)

            # apply the action
            obs, reward, done, _, info = env.step(action)

            # render the env
            env.render()

            time.sleep(0.2)

    # close the env
    env.close()




