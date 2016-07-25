

import numpy as np
from openapscontrib.predict import predict


class ScheinerWalshModel (object):
  def __init__ (self, glucose=[], treatments=[]):
    self.glucose = glucose
    self.insulin = treatments


  def act (self, act):
    pass

  @classmethod
  def from_archive (Klass, selection):
    pass
