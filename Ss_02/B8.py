def isTriangle(a, b, c):
    if a + b > c and a + c > b and b + c > a:
        return True
    return False


print(isTriangle(3, 4, 5))