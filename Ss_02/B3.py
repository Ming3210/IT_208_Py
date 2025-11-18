input = int(input("Nhập một số nguyên: "))


if (input % 3 & input % 5 == 0):
    print("Số vừa nhập chia hết cho cả 3 và 5")
elif (input % 3 == 0):
    print("Số vừa nhập chỉ chia hết cho 3")
elif (input % 5 == 0):
    print("Số vừa nhập chỉ chia hết cho 5")