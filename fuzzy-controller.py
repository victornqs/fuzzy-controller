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

rule1 = ctrl.Rule(PressaoSuccao['B'] | Erro['MMB'], Atuador['MMB'])
rule2 = ctrl.Rule(PressaoSuccao['B'] | Erro['MB'], Atuador['MB'])
rule3 = ctrl.Rule(PressaoSuccao['B'] | Erro['B'], Atuador['MB'])
rule4 = ctrl.Rule(PressaoSuccao['B'] | Erro['M'], Atuador['B'])
rule5 = ctrl.Rule(PressaoSuccao['B'] | Erro['A'], Atuador['B'])
rule6 = ctrl.Rule(PressaoSuccao['B'] | Erro['MA'], Atuador['B'])
rule7 = ctrl.Rule(PressaoSuccao['B'] | Erro['MMA'], Atuador['B'])

rule8 = ctrl.Rule(PressaoSuccao['M'] | Erro['MMB'], Atuador['MB'])
rule9 = ctrl.Rule(PressaoSuccao['M'] | Erro['MB'], Atuador['B'])
rule10 = ctrl.Rule(PressaoSuccao['M'] | Erro['B'], Atuador['B'])
rule11 = ctrl.Rule(PressaoSuccao['M'] | Erro['M'], Atuador['M'])
rule12 = ctrl.Rule(PressaoSuccao['M'] | Erro['A'], Atuador['A'])
rule13 = ctrl.Rule(PressaoSuccao['M'] | Erro['MA'], Atuador['A'])
rule14 = ctrl.Rule(PressaoSuccao['M'] | Erro['MMA'], Atuador['MA'])

rule15 = ctrl.Rule(PressaoSuccao['A'] | Erro['MMB'], Atuador['MMB'])
rule16 = ctrl.Rule(PressaoSuccao['A'] | Erro['MB'], Atuador['MB'])
rule17 = ctrl.Rule(PressaoSuccao['A'] | Erro['B'], Atuador['B'])
rule18 = ctrl.Rule(PressaoSuccao['A'] | Erro['M'], Atuador['M'])
rule19 = ctrl.Rule(PressaoSuccao['A'] | Erro['A'], Atuador['A'])
rule20 = ctrl.Rule(PressaoSuccao['A'] | Erro['MA'], Atuador['MA'])
rule21 = ctrl.Rule(PressaoSuccao['A'] | Erro['MMA'], Atuador['MMA'])

"""
Control System Creation and Simulation
---------------------------------------

Now that we have our rules defined, we can simply create a control system
via:
"""

Atuadorping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21])


Atuadorping = ctrl.ControlSystemSimulation(Atuadorping_ctrl)

# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
Atuadorping.input['PressaoSuccao'] = 15
Atuadorping.input['Erro'] = 5


# Crunch the numbers
Atuadorping.compute()

print (Atuadorping.output['Atuador'])
Atuador.view(sim=Atuadorping)


#rule1.view()
#rule2.view()
#rule3.view()
#rule4.view()
#rule5.view()
#rule6.view()
#rule7.view()
#rule8.view()
#rule9.view()


sim = ctrl.ControlSystemSimulation(Atuadorping_ctrl, flush_after_run=21 * 21 + 1)
"""
View the control space
----------------------

With helpful use of Matplotlib and repeated simulations, we can observe what
the entire control system surface looks like in three dimensions!
"""
# We can simulate at higher resolution with full accuracy
upsampled = np.linspace(-2, 2, 21)
x, y = np.meshgrid(upsampled, upsampled)
z = np.zeros_like(x)

# Loop through the system 21*21 times to collect the control surface
for i in range(21):
    for j in range(21):
        sim.input['PressaoSuccao'] = x[i, j]
        sim.input['Erro'] = y[i, j]
        sim.compute()
        z[i, j] = sim.output['Atuador']

# Plot the result in pretty 3D with alpha blending
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                       linewidth=0.4, antialiased=True)

cset = ax.contourf(x, y, z, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='x', offset=3, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='y', offset=3, cmap='viridis', alpha=0.5)

ax.view_init(30, 200)
