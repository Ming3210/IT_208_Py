input = input("Nhập một số nguyên: ")

for i in range((len(input)-1)//2, -1, -1):
    if input[i] != input[len(input)-1-i]:
        print("Không phải số đối xứng")
        break
else:
    print("Là số đối xứng")
