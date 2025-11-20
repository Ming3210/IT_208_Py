import sys

products = []


def isExist(value):
    newProducts = []
    for i in products:
        newProducts.append(i["id"])
    if newProducts.__contains__(value):
        return True
    else:
        return False


def addProduct():
    id = input("Nhap ma san pham: ")
    while isExist(id) is True:
        print("Id trung lap.")
        id = input("Nhap ma san pham: ")
    name = input("Nhap ten san pham: ")
    quantity = int(input("Nhap so luong: "))
    price = float(input("nhap gia san pham: "))
    product = {
        "id": id,
        "detail": {
            "name": name, "quantity": quantity, "price": price
        }
    }
    products.append(product)


def showProduct():
    for value in products:
        print(value)


def searchProduct(id):
    found = False
    for p in products:
        if p["id"] == id:
            print("San pham tim thay:", p)
            found = True
            break
    if not found:
        print("Khong tim thay san pham")


def updateProduct(id):
    found = False
    for p in products:
        if p["id"] == id:
            print("Nhap thong tin moi (bo trong neu giu nguyen):")
            name = input("Ten moi: ")
            quantity = input("So luong moi: ")
            price = input("Gia moi: ")

            if name != "":
                p["detail"]["name"] = name
            if quantity != "":
                p["detail"]["quantity"] = int(quantity)
            if price != "":
                p["detail"]["price"] = float(price)

            print("Cap nhat thanh cong:", p)
            found = True
            break
    if not found:
        print("Khong tim thay san pham de cap nhat")


def deleteProduct(id):
    found = False
    for p in products:
        if p["id"] == id:
            products.remove(p)
            print("Da xoa san pham:", id)
            found = True
            break
    if not found:
        print("Khong tim thay san pham de xoa")


def userInput():
    result = input("Chon chuc nang: ")
    if result == "1":
        addProduct()
        userInput()
    elif result == "2":
        showProduct()
        userInput()
    elif result == "3":
        print("Tim kiem san pham theo ma")
        id = input("Nhap ma san pham: ")
        searchProduct(id)
        userInput()
    elif result == "4":
        print("Cap nhat thong tin san pham")
        id = input("Nhap ma san pham: ")
        updateProduct(id)
        userInput()
    elif result == "5":
        print("Xoa san pham theo ma san pham")
        id = input("Nhap ma san pham: ")
        deleteProduct(id)
        userInput()
    elif result == "0":
        sys.exit("Dang thoat chuong trinh")
    else:
        print("Chuc nang ko hop le.")
        userInput()


def menu():
    print("============= MENU ================")
    print("1. Them san pham moi")
    print("2. Hien thi danh sach san pham")
    print("3. Tim kiem san pham theo ma")
    print("4. Cap nhat thong tin san pham")
    print("5. Xoa san pham theo ma san pham")
    print("0. Thoat chuong trinh")
    userInput()


menu()
