import gym
import time
from gym_senet.envs.senet import Senet, SenetGame
from agents.random_agent import RandomAgent

env = gym.make('gym_senet:senet-v0', render_mode='human', rules='skyruk')

if __name__ == '__main__':

    agents = {Senet.CONS_PLAYER: RandomAgent('CONS'), Senet.SPOOLS_PLAYER: RandomAgent('SPOOLS')}

    for _ in range(2):

        obs, info = env.reset()
        rules = info['rules']
        legal_actions_fn, _ = SenetGame.gameplay(rules)

        env.render()

        time.sleep(1)

        done = False
        while not done:

            board, player = obs

            # active player
            agent = agents[player]

            # obtain legal actions
            sticks = Senet.throw_sticks()
            legal_actions = legal_actions_fn(board, player, Senet.steps(sticks))

            # choose action
            action = agent.act(legal_actions)

            # apply the action
            obs, reward, done, _, info = env.step(action)

            # render the env
            env.render()

            time.sleep(0.2)

    # close the env
    env.close()




