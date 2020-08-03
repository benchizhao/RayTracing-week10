import numpy as np
import input
import Radiation_Force
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import timeit
import pickle
from drag_force import DragForce
import Power
def mass():
    r = input.radius
    V = 4 / 3 * np.pi * r ** 3
    m = input.density * V
    return m

def gravity():
    N = mass()*input.g
    return np.array([-N, float(0.)])

def drag_force(v,t):
    DF = DragForce(temperature=300, v=v)
    F = DF.drag_force(t)
    return F

def total_force(ray_state):
    tot = np.array([0, 0])
    tot = Radiation_Force.radiation_force(ray_state) + tot
    tot = gravity() + tot
    return tot

def acc(ray_state):
    return total_force(ray_state)/mass()

def stable_point(rang):
    x = np.linspace(rang[0],rang[1],50)
    plt.figure(3)
    for i in x:
        a = acc([i,0,0,0])[0]
        print(i, a)
        plt.plot(i,a,'k.')
    plt.title('Acceleration of the droplet when moving on x-axis')
    plt.xlabel('x position of droplet')
    plt.ylabel('Acceleration on x axis')
    plt.grid()
    plt.show()


def diff2(d_list, t):
    # start = timeit.default_timer()
    x, y = d_list[0:2]
    vx, vy = d_list[2:4]
    tot = np.array([0, 0])
    #
    Power.square_power(time_interval=[0.15, 0.16], t=t)
    # Power.const_power()
    if if_radiation == True:
        tot = Radiation_Force.radiation_force(d_list) + tot
    if if_gravity == True:
        tot = gravity() + tot
    if if_drag == True:
        v = np.array([vx, vy])
        tot = tot - drag_force(v, t)
    ax, ay = tot/mass()

    print(t, input.power)
    # print('x=',x,'tot force=', tot)
    # print('acc=', tot/mass())
    # print(np.array([x,y,vx,vy,ax,ay])*1E6)
    # print('tot force = ',tot)
    print('x=', x, 'y=', y, 'vx=',vx,'vy=',vy)
    # stop = timeit.default_timer()
    return np.array([vx, vy, ax, ay])



if __name__ == '__main__':
    if_radiation = True
    if_gravity = True
    if_drag = True
    # print(mass()*input.g)
    # print(Radiation_Force.radiation_force(input.droplet_pos))
    # print(drag_force(input.droplet_pos[2:4]))
    # print(input.n)
    # print(drag_force(v))
    # print(drag_force(np.array([10,0]))/mass())
    # print(Radiation_Force.radiation_force(input.droplet_pos))
    # stable_point([800E-6,910E-6])




    start = timeit.default_timer()

    # t = np.linspace(0, 0.3, 3000)
    # result = odeint(diff2, input.droplet_pos, t)
    # #
    # f = open('all_on_power_off[0.15,0.16].txt', 'wb')
    # pickle.dump(result, f)
    # f.close()
    # # #


    '''
    Plot 4 figures: x-position, x-velocity, y-position, y-velocity respect to time
    '''
    f = open('all_on_power_off[0.15,0.16].txt', 'rb')
    d = pickle.load(f)
    f.close()
    print(d)

    t = np.linspace(0, 0.3, 3000)

    plt.figure('x-position of droplet power_off[0.15,0.16]')
    plt.plot(t, d[:, 0])
    plt.title('x-position of droplet')
    plt.xlabel('Time (s)')
    plt.ylabel('x-axis')
    # plt.ylim(0,900E-6)
    plt.grid()
    plt.show()

    plt.figure('y-position of droplet power_off[0.15,0.16]')
    plt.plot(t, d[:, 1])
    plt.title('y-position of droplet')
    plt.xlabel('Time (s)')
    plt.ylabel('y-axis')
    plt.grid()
    plt.show()

    plt.figure('x_velocity of droplet power_off[0.15,0.16]')
    plt.plot(t, d[:, 2])
    plt.title('x_velocity of droplet')
    plt.xlabel('Time (s)')
    plt.ylabel('x-velocity')
    plt.grid()
    plt.show()

    plt.figure('y_velocity of droplet power_off[0.15,0.16]')
    plt.plot(t, d[:, 3])
    plt.title('y_velocity of droplet')
    plt.xlabel('Time (s)')
    plt.ylabel('y-velocity')
    plt.grid()
    plt.show()

    # plt.figure('x position respect to x velocity')
    # plt.plot(d[:,0], d[:, 2])
    # plt.title('x position respect to x velocity')
    # plt.xlabel('x position')
    # plt.ylabel('x velocity')
    # plt.grid()
    # plt.show()

    # plt.figure('y position respect to y velocity')
    # plt.plot(d[:, 1], d[:, 3])
    # plt.title('y position respect to y velocity')
    # plt.xlabel('y position')
    # plt.ylabel('y velocity')
    # plt.grid()
    # plt.show()

    stop = timeit.default_timer()
    print('Time: ', stop - start)

