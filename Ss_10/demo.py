import seaborn as sns
import matplotlib.pyplot as plt


sns.set_theme(style="whitegrid")


data_demo = sns.load_dataset("penguins", data_home="data")

plt.figure(figsize=(8, 6))


sns.histplot(data_demo, color="red")
plt.title("Biểu đồ bằng")
plt.xlabel("Tgian")
plt.ylabel("Doanh thu")
plt.show()