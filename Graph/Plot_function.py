import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2, 2, 400)
y = np.sin(2 * np.pi * x)

plt.plot(x, y)
plt.title("Sine Wave")
plt.xlabel("x")
plt.ylabel("sin(2πx)")
plt.grid(True)
plt.show()
