#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
A system of ODEs (ordinary differential equations) of any order can always be
rewritten as a set of first-order equations.

by Tommy Ogden <t.p.ogden@durham.ac.uk>

"""

import sys
import numpy as np

def ode_int(func, y_0, t, method, args={}):
    """ approximation to an first-order ODE system with initial
    conditions.    
        Args:
        func: (callable) The first-order ODE system to be approximated.
        y_0: (array) The initial condition.
        t: (array) A sequence of time points for which to solve for y.
        method: 'ee', 'ie', 'rk', 'ie', 'ab'
        args: (dict) Extra arguments to pass to function.

    Out:
        y: (array) the approximated solution of the system at each time in t,
            with the initial value y_0 in the first row.
    """
    if method == 'ee':
        y = ode_int_ee(func, y_0, t, args)

    elif method == 'rk':
        y = ode_int_rk(func, y_0, t, args)

    elif method == 'ie':
        y = ode_int_ie(func, y_0, t, args)

    elif method == 'ab':
        y = ode_int_ab(func, y_0, t, args)

    return y

def ode_int_ee(func, y_0, t, args={}):
    """ Explicit Euler approximation to an first-order ODE system with initial
    conditions.

    Args:
        func: (callable) The first-order ODE system to be approximated.
        y_0: (array) The initial condition.
        t: (array) A sequence of time points for which to solve for y.
        args: (dict) Extra arguments to pass to function.

    Out:
        y: (array) the approximated solution of the system at each time in t,
            with the initial value y_0 in the first row.

    """

    y = np.zeros([len(t), len(y_0)]) # Initialise the approximation array
    y[0] = y_0

    for i, t_i in enumerate(t[:-1]): # Loop through the time steps

        h = t[i+1] - t_i # size of the step
        y[i+1] = y[i] + h*func(t_i, y[i], args) # Euler step

    return y

def ode_int_rk(func, y_0, t, args={}):
    """ Classical Runge-Kutta (RK4) approximation to a first-order ODE system
    with initial conditions.

    Args:
        func: (callable) The first-order ODE system to be approximated.
        y_0: (array) The initial condition.
        t: (array) A sequence of time points for which to solve for y.
        args: (dict) Extra arguments to pass to function.

    Out:
        y: (array) the approximated solution of the system at each time in t,
            with the initial value y_0 in the first row.

    """

    # Initialise the approximation array
    y = np.zeros([len(t), len(y_0)])
    y[0] = y_0

    # Loop through the time steps, approximating this step from the prev step
    for i, t_i in enumerate(t[:-1]):

        h = t[i+1] - t_i # size of the step

        k_1 = func(t_i, y[i], args)
        k_2 = func(t_i+h/2., y[i]+h/2.*k_1, args)
        k_3 = func(t_i+h/2., y[i]+h/2.*k_2, args)
        k_4 = func(t_i+h, y[i]+h*k_3, args)

        y[i+1] = y[i] + h/6.*(k_1 + 2.*k_2 + 2.*k_3 + k_4) # RK4 step

    return y

def ode_int_ie(func, y_0, t, args={}):
    """ Implicit Euler approximation to an first-order ODE system with initial
    conditions. Predictor-Corrector using the Explicit Euler for the predictor
    step.

    Args:
        func: (callable) The first-order ODE system to be approximated.
        y_0: (array) The initial condition.
        t: (array) A sequence of time points for which to solve for y.
        args: (dict) Extra arguments to pass to function.

    Out:
        y: (array) the approximated solution of the system at each time in t,
            with the initial value y_0 in the first row.
    """

    # Initialise the approximation array
    y = np.zeros([len(t), len(y_0)])
    y[0] = y_0

    # Loop through the time steps
    for i, t_i in enumerate(t[:-1]):

        h = t[i+1] - t_i # size of the step

        y_p = y[i] + h*func(t_i, y[i], args) # Predict (Explicit Euler!)
        y[i+1] = y[i] + h*func(t[i+1], y_p, args) # Corrector

    return y

def ode_int_ab(func, y_0, t, args={}):
    """ Two-Step Adams-Bashforth approximation to a first-order ODE system
    with initial conditions.

    Args:
        func: (callable) The first-order ODE system to be approximated.
        y_0: (array) The initial condition.
        t: (array) A sequence of time points for which to solve for y.
        args: (dict) Extra arguments to pass to function.

    Out:
        y: (array) the approximated solution of the system at each time in t,
            with the initial value y_0 in the first row.        
    """

    # Initialise the approximation array
    y = np.zeros([len(t), len(y_0)])
    y[0] = y_0

### Step 0: Euler

    h = t[1] - t[0]
    y[1] = y[0] + h*func(t[0], y[0], args) # Euler step

### Step 1: Adams-Bashforth, Different Stepsizes

    h_1 = t[1] - t[0]
    h_2 = t[2] - t[1]

    y[2] = y[1] + 0.5*h_2/h_1*((2.*h_1 + h_2)*func(t[1], y[1], args) -
                       h_2*func(t[0], y[0], args))

### Steps 2 to N-1: Adams-Bashforth

    # Loop through the time steps
    for i, t_i in enumerate(t[2:-1], start=2):

        h = t[i+1] - t_i # size of the step
        y[i+1] = y[i] + (1.5*h*func(t_i, y[i], args) -
                         0.5*h*func(t[i-1], y[i-1], args)) # Adams-Bashforth

    return y

def main():
    pass

if __name__ == '__main__':
    status = main()
    sys.exit(status)