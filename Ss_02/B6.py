input = int(input("Nhập một số nguyên: "))
result = 1
if (input < 0):
    print("Số vừa nhập là số âm")
else:
    for i in range(1, input + 1):
        result = result * i
print(result)