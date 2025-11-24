import numpy as np
arr = np.random.randint(30, size=(3, 3, 3))

reverse = np.linalg.inv(arr)

einvalues, einvectors = np.linalg.eig(arr)

print("Gia tri dao:\n", reverse)

print("\n")
print("\n")
print("\n")
print("\n")

print("Gia tri rieng:\n", einvalues)

print("\n")
print("\n")
print("\n")
print("\n")

print("Vec to rieng:\n", einvectors)