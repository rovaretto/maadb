"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


fig, ax = plt.subplots(1, 1)
mu, sigma = 1.59792, 0.674185
X = stats.norm(loc=mu, scale=sigma)
Y = stats.lognorm(s=sigma, scale=np.exp(mu))
x = np.linspace(*X.interval(0.999))
y = Y.rvs(size=10000)
ax.plot(x, X.pdf(x), label='X (pdf)')
ax.plot(x, Y.pdf(x), label='')
ax.legend()
plt.show()

print(y)

"""
import numpy
from numpy import random

res1 = random.lognormal(mean=1.156550732, sigma=0.605779837, size=10)
print(res1)

res2 = random.lognormal(mean=0.910107586603591, sigma=0.5566766882, size=10)
print(res2)

res3 = random.lognormal(mean=2.452519925, sigma=0.6446728932, size=10)
print(res3)

res4 = random.lognormal(mean=0.4838759874, sigma=0.5248368908, size=10)
print(res4)

res = res1 + res2 + res3 + res4

print(numpy.ceil(res))
