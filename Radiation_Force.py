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
import timeit
import matplotlib.pyplot as plt

import movement
import showAshkin as SA

# all_forwards = []
# all_backwards = []
def intensity(position):
    I = []
    for i in range(len(position)):
        intens = NonABCD.gaussian(position[i], input.sigma)
        I.append(intens)
    normalise_I = I / sum(I)
    return normalise_I

def bundle(ray_state):
    list_of_rays = np.linspace(-input.width, input.width, input.no_of_rays)
    all_forwards = []
    all_backwards = []
    for i in range(input.no_of_rays):
        NonABCD.ray(0, list_of_rays[i] + input.y_displacement, 0, intensity(list_of_rays)[i])
        NonABCD.lens_trace(input.lens_f, input.lens_pos, input.len_thickness)
        NonABCD.free_propagate(10E-6)
        NonABCD.propagate(ray_state[0] - input.lens_pos - 10E-6)
        NonABCD.circle(input.radius,ray_state)
        NonABCD.free_propagate(15E-6)
        NonABCD.propagate(200E-6)
        a = copy.deepcopy(NonABCD.forward)
        # b = copy.deepcopy(NonABCD.backward)
        all_forwards = all_forwards + [a]
        # all_backwards = all_backwards + [b]
        NonABCD.forward.clear()
        NonABCD.backward.clear()
    return all_forwards #all_backwards



def useful_data_for(ray_state):
    '''
    Clean the data, some rays in all_forwards will not interact with the droplet, which are useless.
    This function will keep those rays interact with the droplet and delete those rays have no interaction with the droplet.
    '''
    all_forwards = bundle(ray_state)
    useful_for = [i for i in all_forwards]
    for i in range(len(useful_for)-1,-1,-1): # iterate from right to left
        if len(useful_for[i]) != 12:
            useful_for.pop(i)
    return useful_for

def useful_data_back(ray_state):
    '''
    Clean the data, some rays in all_backwards will not interact with the droplet, which are useless.
    This function will keep those rays interact with the droplet and delete those rays have no interaction with the droplet.
    '''
    all_backwards = bundle(ray_state)[1]
    useful_back = [i for i in all_backwards]
    for i in range(len(useful_back)-1,-1,-1): # iterate from right to left
        if len(useful_back[i]) != 12:
            useful_back.pop(i)
    return useful_back

def F_s(ray_state,data):
    '''
    Calculate the scattering force.
    :return total_forcr: list
        The total_foce contains two element, the first one is the force along x-aixs, and the second one is the force along y-axis.
    '''

    # data = useful_data_for(ray_state)
    force = []
    total_force = np.array([0, 0])
    # plt.figure()
    for i in range(len(data)):
        x = data[i][6][0]
        y = data[i][6][1]
        vec_1 = [x-ray_state[0], y-ray_state[1]]
        vec_2 = [-1, -np.tan(data[i][6][2])]
        unit_vector_1 = vec_1 / np.linalg.norm(vec_1)
        unit_vector_2 = vec_2 / np.linalg.norm(vec_2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        theta1 = np.arccos(dot_product)
        theta2 = NonABCD.snell(theta1)  # Refracted angle

        # print(data[i][6][2],theta1,theta2)
        P = input.power * data[i][6][3]
        F = input.medium_n * P / input.c*(1+NonABCD.R(theta1)*np.cos(2*theta1)- (NonABCD.T(theta1) ** 2 * (np.cos(2 * theta1 - 2 * theta2) + NonABCD.R(theta1) * np.cos(2 * theta1))) / (1 + NonABCD.R(theta1) ** 2 + 2 * NonABCD.R(theta1) * np.cos(2 * theta2)))
        # print(input.medium_n * P / input.c )
        Fx = abs(F) * np.cos(data[i][6][2])
        Fy = abs(F) * np.sin(data[i][6][2])
        # plt.plot(y,abs(F),'.')
        force.append([Fx, Fy])
        total_force = total_force + np.array([Fx, Fy])
    # plt.show()
    return total_force

def F_g(ray_state, data):
    '''
        Calculate the gradient force.
        :return total_forcr: list
            The total_foce contains two element, the first one is the force along x-aixs, and the second one is the force along y-axis.
        '''
    # data = useful_data_for(ray_state)
    total_force = np.array([0, 0])
    # print(np.shape(data))
    for i in range(len(data)):
        x = data[i][6][0]
        y = data[i][6][1]
        vec_1 = [x - ray_state[0], y - ray_state[1]]
        vec_2 = [-1, -np.tan(data[i][6][2])]
        unit_vector_1 = vec_1 / np.linalg.norm(vec_1)
        unit_vector_2 = vec_2 / np.linalg.norm(vec_2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        theta1 = np.arccos(dot_product)
        theta2 = NonABCD.snell(theta1) # Refracted angle

        # print(y, data[i][6][2]/np.pi*180, theta1/np.pi*180, theta2/np.pi*360)
        P = input.power * data[i][6][3]
        F = input.medium_n*P/input.c *(NonABCD.R(theta1)*np.sin(2*theta1)-(NonABCD.T(theta1)**2*(np.sin(2*theta1-2*theta2)+NonABCD.R(theta1)*np.sin(2*theta1)))/(1+NonABCD.R(theta1)**2+2*NonABCD.R(theta1)*np.cos(2*theta2)))
        if data[i][6][2] < np.pi:
            Fx = abs(F) * np.cos(data[i][6][2]-np.pi/2)
            Fy = abs(F) * np.sin(data[i][6][2]-np.pi/2)
        else:
            Fx = abs(F) * np.cos(data[i][6][2] + np.pi / 2)
            Fy = abs(F) * np.sin(data[i][6][2] + np.pi / 2)
        # print(y, Fx, Fy, i)
        total_force = total_force + np.array([Fx, Fy])
        # print(total_force)
    return total_force

def radiation_force(ray_state):
    # useful_data_for(ray_state)
    data = useful_data_for(ray_state)
    Force = F_g(ray_state, data) + F_s(ray_state, data)
    return Force

if __name__ == '__main__':
    def inter(x_range, y_range):
        x = np.linspace(x_range[0], x_range[1], 100)
        y = np.linspace(y_range[0], y_range[1], 100)
        plt.figure()
        for i in range(len(x)):
            ray_state = [x[i], y[i], 0, 0]
            print(i)
            data = useful_data_for(ray_state)
            # print(x[i], np.shape(useful_data_for(ray_state)),F_g(ray_state))
            plt.plot(y[i], F_g(ray_state, data)[1], 'k.')
            # plt.plot(x[i], F_s(ray_state, data)[0] + movement.gravity()[0], 'g.')
            # print(F_s(), F_g())
            # print(np.shape(all_forwards),np.shape(useful_data_for()))
        plt.title('y position respect to force')
        plt.xlabel('y position')
        plt.ylabel('y force')
        plt.grid()
        plt.show()

    start = timeit.default_timer()
    # ray_state = input.droplet_pos
    # data = useful_data_for(ray_state)
    # Force = F_g(ray_state, data) + F_s(ray_state, data)
    # f2 = radiation_force(ray_state)
    # print(np.shape(data))
    # print(Force)
    # print(f2)
    # bundle(input.droplet_pos)
    # useful_data_for()
    # print(np.shape(useful_data_for()))
    # print(input.droplet_pos)
    # print(radiation_force([504, 0, 0, 0]))
    inter([850E-6,850E-6],[-10E-6,10E-6])
    # print(F_g(input.droplet_pos))
    # print(F_s(input.droplet_pos))
    # bundle(input.droplet_pos)
    # F_s(input.droplet_pos)
    stop = timeit.default_timer()
    print('Time: ', stop - start)

