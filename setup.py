from setuptools import setup
import gym_senet

setup(name='gym_senet',
      version=gym_senet.__version__,
      install_requires=['numpy', 'gym', 'pyglet']
)