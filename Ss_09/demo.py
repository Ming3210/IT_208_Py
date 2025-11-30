import matplotlib.pyplot as plt

import numpy as np

fig, ax = plt.subplots(figsize=(8, 6))

x = np.random.randint(1, 10, 10)
y = x**2

ax.grid()
ax.set_title("Biểu đồ bằng")
ax.plot(x, y)

plt.show()