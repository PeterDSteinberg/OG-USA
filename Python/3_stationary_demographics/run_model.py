'''
This will run the steady state solver as well as time path iteration.
'''

import numpy as np
import pickle
import os
from glob import glob

# Run steady state
run_SS = True
run_TPI = False

'''
------------------------------------------------------------------------
Setting up the Model
------------------------------------------------------------------------
S            = number of periods an individual lives
J            = number of different ability groups
T            = number of time periods until steady state is reached
starting_age = age of first members of cohort
beta         = discount factor
sigma        = coefficient of relative risk aversion
alpha        = capital share of income
nu           = contraction parameter in steady state iteration process
               representing the weight on the new distribution gamma_new
A            = total factor productivity parameter in firms' production
               function
delta        = depreciation rate of capital
ctilde       = minimum value amount of consumption
ltilde       = measure of time each individual is endowed with each
               period
chi          = discount factor
eta          = Frisch elasticity of labor supply
e            = S x J matrix of age dependent possible working abilities
               e_s
T            = number of periods until the steady state
omega        = T x S x J array of demographics
TPImaxiter   = Maximum number of iterations that TPI will undergo
TPImindist   = Cut-off distance between iterations for TPI
------------------------------------------------------------------------
'''


# Parameters
S = 60
J = 1
T = int(1.5 * S)
starting_age = 20
beta_annual = .96
beta = beta_annual ** (60.0 / S)
sigma = 3.0
alpha = .35
nu = .20
A = 1.0
delta_annual = .05
delta = 1 - ((1-delta_annual) ** (60.0 / S))
ctilde = .001
ltilde = 1.0
chi = 1.0
eta = 2.0
g_y_annual = 0.03
g_y = (1 + g_y_annual)**(60.0/S) - 1
TPImaxiter = 100
TPImindist = 3 * 1e-6

print 'Saving user given parameter values.'
var_names = ['S', 'J', 'T', 'starting_age', 'beta', 'sigma',
             'alpha', 'nu', 'A', 'delta', 'ctilde', 'ltilde',
             'chi', 'eta', 'g_y', 'TPImaxiter', 'TPImindist']
dictionary = {}
for key in var_names:
    dictionary[key] = globals()[key]
pickle.dump(dictionary, open("OUTPUT/given_params.pkl", "w"))
print '\tFinished.'


if run_SS:
    import SS

if run_TPI:
    import TPI

'''
See the pickles for results.
'''

'''
Delete all .pyc files that have been generated
'''

files = glob('*.pyc')
for i in files:
    os.remove(i)
