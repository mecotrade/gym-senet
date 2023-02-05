from gym.envs.registration import register
from .version import version as __version__

register(
    id='senet-v0',
    entry_point='gym_senet.envs:SenetEnv'
)
