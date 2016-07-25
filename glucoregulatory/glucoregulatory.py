"""
A model of the human glucoregulatory system provided by
openaps-predict: https://github.com/loudnate/openaps-predict
which uses the Walsh IOB algorithm to determine effect of
added insulin on glucose level.
"""

import logging
from gym import spaces
from gym.utils import seeding
import numpy as np

import openapscontrib.predict as predict

logging.info("imports succeeded")

class GlucoregulatoryEnv(gym.Env):

    def __init__(self, seed=None, history=None):
        """
        We need to initialize some random BGL and start inserting events.
        Open question: what's our time delta? probably nice to put that in
        as a parameter.

        Perhaps starting BGL should also be a random number within some
        bounds with a seed passed in as a default parameter.
        """

        # BGL in which to declare the episode failed [mg/dL (?)]
        self.bgl_threshold_low = 20
        self.bgl_threshold_high = 800
        # Valid amounts of insulin to dose [mg (?)]
        self.low_dose = 0
        self.low_dose = 15 # what should this really be?

        # The action space is single value amount of insulin to give in mg/dL(?)
        self.action_space = spaces.Box(low_dose, high_dose, [1,1])
        # Observation space is a single value BGL
        self.observation_space = spaces.Box(self.bgl_threshold_low, self.bgl_threshold_high, [1,1])

        # Now initialize some history and present state This will be a dict
        # of current bgl, normalized history, normalized glucose, and
        # effects, or those duplicating some things?
        if history is None:
            # generate our own history
        else:
            # we were provided some history, just use that

    def _seed(self, seed=None):
        self.np_random, seed, seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        """
        Take an action and update the model

        Returns standard Env._step tuple:
            observation: object
            reward: float
            done: boolean
            info: dict

        Human operators have many observations that we will not allow the
        pancreas operator to have. For example the GlucoregulatoryEnv can
        decide to do exercise and eat, but our pancreas doesn't directly
        observe those actions. The pancreas observes instantaneous blood
        glucose levels and makes an action of how much insulin to dose.

        The reward will need tuning with time, but the idea is that we want
        to live, and ideally stay within some acceptable blood-glucose level.
        Something like inverse square distance from 100 sounds reasonable for
        now.

        I guess we can provide the actions such as eating and exercise as
        info
        """

        return observation, reward, done, info
