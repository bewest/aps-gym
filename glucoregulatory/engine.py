

import numpy as np
# from openapscontrib.predict import predict
from openapscontrib import predict
from openapscontrib.predict import predict as prepare
from os.path import join


class ScheinerWalshModel (object):
  def __init__ (self, glucose=[], treatments=[], calibrations=[], **kwds):
    self.glucose = glucose
    self.insulin = treatments
    self.original = dict(glucose=glucose, insulin=treatments)
    self.calibrations = calibrations
    self.counts = 0
    self.prediction_time = kwds.get('prediction_time', 30)
    self.carb_ratios = prepare.Schedule(kwds.get('carb_ratios', []))
    self.insulin_sensitivities = prepare.Schedule(kwds.get('insulin_sensitivities', []))
    self.absorption_delay = kwds.get('absorption_delay', 10)
    self.absorption_duration = kwds.get('absorption_duration', None)
    self.insulin_action_curve = kwds.get('insulin_action_curve', None)
    self.insulin_absorption_delay = kwds.get('insulin_absorption_delay', None)


  def get_state (self, effects=[]):
    state = dict(glucose=self.glucose, treatments=self.insulin, calibrations=calibrations, counts=self.counts, effects=effects)
    return state
  def get_momentum_effect (self, prediction_time=None):
    prediction_time = prediction_time or self.prediction_time
    return predict.calculate_momentum_effect((self.glucose), prediction_time=prediction_time, recent_calibrations=self.calibrations)

  def get_scheiner_carb_effect (self, carb_ratios=None, insulin_sensitivities=None, absorption_delay=None, absorption_duration=None):
    carb_ratios = carb_ratios or self.carb_ratios
    insulin_sensitivities = insulin_sensitivities or self.insulin_sensitivities
    kwds = dict( )
    kwds.update(absorption_duration = absorption_duration or self.absorption_duration)
    kwds.update(absorption_delay = absorption_delay or self.absorption_delay)
    return prepare.calculate_carb_effect(self.insulin, carb_ratios, insulin_sensitivities, **kwds)

  def get_walsh_insulin_effect (self, insulin_action_curve=None, insulin_sensitivities=None, insulin_absorption_delay=None):
    insulin_sensitivities = insulin_sensitivities or self.insulin_sensitivities
    insulin_action_curve = insulin_action_curve or self.insulin_action_curve
    kwds = dict( )
    kwds.update(absorption_delay = insulin_absorption_delay or self.insulin_absorption_delay)
    return prepare.calculate_insulin_effect(self.insulin, insulin_action_curve, insulin_sensitivities, **kwds)

  def get_glucose_momentum_effect (self, dt=5, prediction_time=300, fit_points=3):
    return prepare.calculate_momentum_effect(self.glucose, self.calibrations, dt=dt, prediction_time=prediction_time, fit_points=fit_points)

  def append_action (self, action):
    # self.insulin.append(action)
    return

  def act (self, act):
    """
    """
    # 1. Add action to list of previous actions
    self.append_action(act)
    # 2. Get effects due to new action
    momentum = self.get_momentum_effect( )
    walsh = self.get_walsh_insulin_effect( )
    scheiner = self.get_scheiner_carb_effect( )
    effects = [ walsh, scheiner ]
    # 3. Get new glucose based on these new effects
    new_glucose = prepare.calculate_glucose_from_effects(effects, self.glucose, momentum=momentum)
    self.glucose = new_glucose
    # increment counter
    self.count += 1
    state = self.get_state(dict(momentum=momentum, scheiner=scheiner, walsh=walsh))
    return state

  @classmethod
  def prep_spec (Klass, prefix='~/Documents/foobar', tag='builtin'):
    results = dict( )
    if tag == 'builtin':
      results.update(glucose=prepare._json_file(join(prefix, 'monitor/glucose.json')))
      results.update(calibrations=prepare._opt_json_file(join(prefix, 'monitor/calibrations.json')) or  ())
      crs = dict(carb_ratios=dict(schedule=[]))
      isfs = dict(insulin_sensitivities=dict(sensitivities=[]))
      settings = dict(insulin_action_curve=4)
      results.update(carb_ratios=(prepare._opt_json_file(join(prefix, 'raw-pump/carb-ratios.json')) or crs)['carb_ratios']['schedule'])
      results.update(insulin_sensitivities=(prepare._opt_json_file(join(prefix, 'raw-pump/insulin-sensitivities-raw.json')) or isfs)['insulin_sensitivities']['sensitivities'])
      results.update(insulin_action_curve=(prepare._opt_json_file(join(prefix, 'monitor/settings.json')) or settings)['insulin_action_curve'])


    return results
  @classmethod
  def from_archive (Klass, prefix='~/Documents/foobar', tag='builtin'):
    spec = Klass.prep_spec(prefix=prefix, tag=tag)
    return Klass(**spec)
