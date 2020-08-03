import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle
import imageio
f = open('radiation&drag&gravity.txt', 'rb')
d = pickle.load(f)
f.close()

def update_points(num):
    '''
    更新数据点
    '''
    point_ani.set_data(x[num], y[num])
    return point_ani,

x = d[:,0]
y = d[:,1]
print(y)

# fig = plt.figure(tight_layout=True)
# plt.plot(x, y)
# plt.grid(ls="--")
# plt.show()



fig = plt.figure(tight_layout=True)
plt.plot(x, y)
point_ani, = plt.plot(x[0], y[0], "ro")
plt.grid(ls="--")
# 开始制作动画
ani = animation.FuncAnimation(fig, update_points, np.arange(0, len(x)), interval=10, blit=True)

ani.save('test_animation.gif')
# ani.save('animation.gif', writer='imagemagick', fps=10)
plt.show()