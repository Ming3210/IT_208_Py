import matplotlib.pyplot as plt


month = [1, 2, 3]
cell = [100, 200, 300]

# y = x^3




fig, ax = plt.subplots()
ax.plot(month, cell, color="red", linestyle="-", marker="o")

ax.set_title("Biểu đồ bằng")


ax.set_xlabel("Tgian")
ax.set_ylabel("Doanh thu")

plt.show()