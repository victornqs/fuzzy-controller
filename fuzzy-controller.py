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
# Auto-membership function population is possible with .automf(3, 5, or 7)
#PressaoSuccao.automf(3)
#Erro.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API

# Generate fuzzy membership functions
PressaoSuccao['B'] = fuzz.trapmf(PressaoSuccao.universe, [-0.1, -0.1, 2, 5])
PressaoSuccao['M'] = fuzz.trapmf(PressaoSuccao.universe, [2, 5 , 15, 18])
PressaoSuccao['A'] = fuzz.trapmf(PressaoSuccao.universe, [15, 18, 40, 40])
Erro['MMB'] = fuzz.trapmf(Erro.universe, [-40, -40, -5, -3])
Erro['MB'] = fuzz.trimf(Erro.universe, [-5, -3, -1])
Erro['B'] = fuzz.trimf(Erro.universe, [-3, -1, -0.4])
Erro['M'] = fuzz.trimf(Erro.universe, [-0.5, 0, 0.5])
Erro['A'] = fuzz.trimf(Erro.universe, [0.4, 1, 3])
Erro['MA'] = fuzz.trimf(Erro.universe, [1, 3, 5])
Erro['MMA'] = fuzz.trapmf(Erro.universe, [3, 5, 50, 50])
Atuador['MMB'] = fuzz.trapmf(Atuador.universe, [-10, -10, -3, -1])
Atuador['MB'] = fuzz.trimf(Atuador.universe, [-3, -1, -0.3])
Atuador['B'] = fuzz.trimf(Atuador.universe, [-1, -0.3, 0])
Atuador['M'] = fuzz.trimf(Atuador.universe, [-0.3, 0, 0.3])
Atuador['A'] = fuzz.trimf(Atuador.universe, [0, 0.3, 1])
Atuador['MA'] = fuzz.trimf(Atuador.universe, [0.3, 1, 3])
Atuador['MMA'] = fuzz.trapmf(Atuador.universe, [1, 3, 10, 10])

"""
To help understand what the membership looks like, use the ``view`` methods.
"""

# You can see how these look with .view()
PressaoSuccao['M'].view()
"""
.. image:: PLOT2RST.current_figure
"""
Erro['M'].view()
"""
.. image:: PLOT2RST.current_figure
"""
Atuador['M'].view()
"""
.. image:: PLOT2RST.current_figure


Fuzzy rules
-----------
"""
