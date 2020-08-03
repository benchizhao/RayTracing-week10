import input
import matplotlib.pyplot as plt
import numpy as np

class DragForce:
    def __init__(self, temperature, v):
        self.temperature = temperature
        self.atm_pressure = 101325 #(Pa)
        self.v = v # (m/s)
        self.air_state = 'dry'
        self.radius = input.radius

    def viscosity(self):
        return 2.791E-7 * self.temperature ** 0.7355

    def pressure(self, t):
        # return self.atm_pressure
        p = -800000 * t + self.atm_pressure
        if p > 100:
            return p
        elif p <= 100:
            return 100

    def air_density(self, t):
        if self.air_state == 'dry':
            R = 287.058
            return self.pressure(t)/(R*self.temperature)
        elif self.air_state == 'humid':
            pass

    def Re(self, t):
        # calculate the Reynold number
        return self.air_density(t) * self.v * 2 * self.radius/self.viscosity()

    def mean_free_path(self, t):
        l = np.sqrt(np.pi/8) * self.viscosity()/0.4987445 * 1/np.sqrt(self.air_density(t)*self.pressure(t))
        return l

    def cunningham_correction(self,t):
        Kn = self.mean_free_path(t)/self.radius
        alpha = 1.155
        beta = 0.471
        gamma = 0.596
        return 1 + Kn*(alpha + beta * np.exp(-gamma/Kn))

    def drag_force(self,t):
        F = 6 * np.pi * self.viscosity() * self.radius * self.v
        return F/self.cunningham_correction(t)

if __name__ == '__main__':
    # v = np.array([0.005,0.003])
    # DF = DragForce(300,v)
    # print(DF.atm_pressure)
    # print(DF.air_density())
    # # print(DF.cunningham_correction(0.011))
    # # print(DF.mean_free_path(0.011))
    # # print(DF.viscosity())
    # # print(DF.drag_force(0.011))

    t = np.linspace(0,0.3,1000)
    p = -800000 * t + 101325
    for i in range(len(p)):
        if p[i] < 100:
            p[i] = 100
    plt.figure('pressure vs time')
    plt.plot(t, p)
    plt.title('pressure vs time')
    plt.xlabel('Time (s)')
    plt.ylabel('pressure (Pa)')
    plt.grid()
    plt.show()

