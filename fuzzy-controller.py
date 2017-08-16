"""
Created on Tue Aug 15 16:14:40 2017

@author: victor.barreto

==========================================
Fuzzy Control Systems: Speed Control
==========================================

Controller Using the skfuzzy control API
-------------------------------------------------------------

We can use the `skfuzzy` control system API to model this.  First, let's
define fuzzy variables
"""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl