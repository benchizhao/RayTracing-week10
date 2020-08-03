'''
This file contains all parameter will be used in the following code.
'''
import numpy as np
'''
Ray Tracing parameters
----------------------
'''
# About the beam
ray_type = 'g'  # energy distribution of rays. 'f' represents flat, the intensity of all rays are the same;
                                            #  'g' represent gaussian, the intensity distriburion of rays are gaussian.
polarisation = 'p'  # Type of polarisation: 's', 'p', 'circle'
power = 200E-3 # Total power of the beam.
sigma = 10E-6  # sigma is the parameter to describe the gaussian.
no_of_rays = 400   # Number of rays we are going to trace
width = 40E-6  # Width of the rays
# Refractive index
medium_n = 1    # Refractive index of the surrounding
target_n = 1.5  # Refractive index of the droplet
y_displacement = 0
'''
Parameters for droplet
'''
radius = 10E-6   # (um) radius of the droplet
droplet_pos = np.array([900, 5, 0, 0])*1E-6      # (um)Central position of the droplet [x, y, vx, vy]
density = 960 # kg/m^3
'''
Parameters for lens
'''
lens_pos = 50E-6               # (um)Central position of the lens
lens_f = 200E-6                # (um)Focal length of the lens
len_thickness = 20E-6          # (um)Thickness of the lens

'''
Viscosity drag
'''
rho = 1.293     # kg/m^3
n = 1.8E-5    # kg/(m.s)
'''
Other useful parameters
'''
c = 2.98E+8 # Speed of light
g = 9.8

