import gym
import time
from gym_senet.envs.senet import Senet
from agents.random_agent import RandomAgent

env = gym.make('gym_senet:senet-v0', render_mode='ansi')


if __name__ == '__main__':

    agents = {Senet.CONS_PLAYER: RandomAgent('CONS'), Senet.SPOOLS_PLAYER: RandomAgent('SPOOLS')}

    for _ in range(2):

        obs, info = env.reset()

        print(env.render())

        time.sleep(1)

        done = False
        while not done:

            board, player = obs

            # active player
            agent = agents[player]
            print(f'agent {agent.name} move')

            # throw sticks
            sticks = Senet.throw_sticks()
            print(f'sticks thrown: {sticks}')

            # obtain legal actions
            legal_actions = Senet.legal_moves(board, player, sticks)
            print(f'legal actions: {legal_actions}')

            # choose action
            action = agent.act(legal_actions=legal_actions)
            print(f'agent {agent.name} takes action {action}')

            # apply the action
            obs, reward, done, _, info = env.step(action)

            # render the env
            print(env.render())
            print(f'reward = {reward}')

            time.sleep(0.2)

        print(info)

    # close the env
    env.close()




