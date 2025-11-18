def isPrime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


a = int(input("Nhập một số nguyên a: "))
b = int(input("Nhập một số nguyên b: "))
if a > b:
    print("a lớn hơn b")

for i in range(a, b + 1, 1):
    if isPrime(i):
        print(i)