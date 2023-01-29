from gym.envs.registration import register

register(
    id='senet-v0',
    entry_point='gym_senet.envs:SenetEnv'
)
