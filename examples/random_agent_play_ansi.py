import gym
import time
from gym_senet.envs.senet import Senet, SenetGame
from examples.random_agent import RandomAgent

env = gym.make('gym_senet:senet-v0', render_mode='ansi')

if __name__ == '__main__':

    agents = {Senet.CONS_PLAYER: RandomAgent('CONS'), Senet.SPOOLS_PLAYER: RandomAgent('SPOOLS')}

    for _ in range(2):

        (board, player), info = env.reset()
        rules = info['rules']
        legal_actions_fn, _ = SenetGame.gameplay(rules)

        print(env.render())

        time.sleep(1)

        done = False
        while not done:

            # active player
            agent = agents[player]
            print(f'agent {agent.name} move')

            # throw sticks
            sticks = Senet.throw_sticks()
            print(f'sticks thrown: {sticks}')

            # obtain legal actions
            legal_actions = legal_actions_fn(board, player, Senet.steps(sticks))
            print(f'legal actions: {[Senet.decode_move_for_player(action, board, player) for action in legal_actions]}')

            # choose action
            action = agent.act(legal_actions)
            print(f'agent {agent.name} takes action {Senet.decode_move_for_player(action, board, player)}')

            # apply the action
            (board, player), reward, done, _, info = env.step(action)

            # render the env
            print(env.render())
            print(f'reward = {reward}')

            time.sleep(0.2)

        print(info)

    # close the env
    env.close()




