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

# New Antecedent/Consequent objects hold universe variables and membership
# functions
PressaoSuccao = ctrl.Antecedent(np.arange(-0.1, 40, 1), 'PressaoSuccao')
Erro = ctrl.Antecedent(np.arange(-40, 40, 1), 'Erro')
Atuador = ctrl.Consequent(np.arange(-10, 10, 1), 'Atuador')
