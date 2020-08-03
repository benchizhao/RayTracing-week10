# -*- coding: utf-8 -*-
"""
Time: 2020/Jul/06

@author: Benchi Zhao
Python version: 3.7
Functionality: This module calculate the force caused by radiation pressure.
Dependence: Need import 'NewNonABCD', all parameters of the experiment is saved in that file 'input'.
"""

import sys
import numpy as np
import input
import NewNonABCD as NonABCD
import copy
import matplotlib.pyplot as plt

def drag_force(v):
    F = 6 * np.pi * input.n * input.radius*1E-6 * v
    return F