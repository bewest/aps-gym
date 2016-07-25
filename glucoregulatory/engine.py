
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
from openapscontrib.predict import predict


class ScheinerWalshModel (object):
  def __init__ (self):
    self.glucose = [ ]
    self.insulin = [ ]


  def act (self, act):
    pass

class DiabetesEnv(gym.Env):
  metadata = {
    'render.modes': ['human', 'rgb_array'],
    'video.frames_per_second': 30
  }

  def __init__ (self):
    super(DiabetesEnv, self).__init__( )
    """
    Action space:
    duration: 0 - 30 minutes
    rate: 0 - max_rate_per_hour
    (predicted glucose?)
    (ISF, DIA?)
    """
    self.action_space = spaces.HighLow( )
    """
    Observation space:
    glucose history - last 2 hours
    glucose prediction - via DIA
    insulin history
    ISF
    rate
    duration
    IOB
    COB

    """
    self.observation_space = spaces.Box( )

  def _reset (self):
    pass

  def _step (self, action):
    # get state
    # apply action
    # do_insulin_effect
    # do_carb_effect
    # dose insulin
    # get new state
    # assign reward
    observation = None
    reward = None
    done = False
    info = dict( )
    return (observation, reward, done, info)
