import csv
import matplotlib.pyplot as plt

sts_list = []


def menu():
    print("==================== MENU ====================")
    print("‖ 1. Hiển thị danh sách sinh viên            ‖")
    print("‖ 2. Thêm sinh viên mới                      ‖")
    print("‖ 3. Cập nhật thông tin sinh viên            ‖")
    print("‖ 4. Xóa sinh viên                           ‖")
    print("‖ 5. Tìm kiếm sinh viên                      ‖")
    print("‖ 6. Sắp xếp danh sách sinh viên             ‖")
    print("‖ 7. Thống kê điểm TB                        ‖")
    print("‖ 8. Vẽ biểu đồ thống kê điểm TB             ‖")
    print("‖ 9. Lưu vào file CSV                        ‖")
    print("‖ 10. Thoát chương trình                     ‖")
    print("==============================================")


def show_all_students():
    with open('students.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        sts_list.clear()
        for row in reader:
            row['diem_toan'] = float(row['diem_toan'])
            row['diem_ly'] = float(row['diem_ly'])
            row['diem_hoa'] = float(row['diem_hoa'])
            row['diem_tb'] = float(row['diem_tb'])
            sts_list.append(row)
    for student in sts_list:
        print(student)


def input_sts():
    name = input("Nhập tên sinh viên: ")
    math_score = float(input("Nhập điểm Toán: "))
    physics_score = float(input("Nhập điểm Lý: "))
    chemistry_score = float(input("Nhập điểm Hóa: "))
    student_id = f"SV{len(sts_list) + 1:03d}"
    avg_score = round((math_score + physics_score + chemistry_score) / 3, 2)
    if avg_score >= 8.0:
        classification = "Giỏi"
    elif avg_score >= 6.5:
        classification = "Khá"
    elif avg_score >= 5.0:
        classification = "Trung Bình"
    else:
        classification = "Yếu"
    student = {
        "id": student_id,
        "ten": name,
        "diem_toan": math_score,
        "diem_ly": physics_score,
        "diem_hoa": chemistry_score,
        "diem_tb": avg_score,
        "xep_loai": classification
    }
    return student


def add_students():

    student = input_sts()
    sts_list.append(student)

    print("Thêm sinh viên mới thành công.")


def update_students(id):
    for sts in sts_list:
        if sts["id"] == id:
            print("Cập nhật thông tin cho sinh viên:", sts["ten"])
            updated_sts = input_sts()
            sts.update(updated_sts)
            print("Cập nhật thông tin sinh viên thành công.")
            return
        else:
            print("Không tìm thấy sinh viên với ID đã cho.")


def del_students(id):
    for sts in sts_list:
        if sts["id"] == id:
            sts_list.remove(sts)
            print("Xóa sinh viên thành công.")
            return
    print("Không tìm thấy sinh viên với ID đã cho.")


def search_students(keyword):
    for sts in sts_list:
        if (
            keyword.lower() in sts["ten"].lower()
            or keyword.lower() in sts["id"].lower()
        ):
            print(sts)


def sort_menu():
    print("Chọn kiểu sắp xếp:")
    print("1. Sắp xếp theo tên (tăng dần)")
    print("2. Sắp xếp theo tên (giảm dần)")
    print("3. Sắp xếp theo điểm TB (tăng dần)")
    print("4. Sắp xếp theo điểm TB (giảm dần)")
    print("5. Quay lại menu chính")
    print("Lựa chọn: ", end="")
    return int(input())


def sort_students(sort_type, isAsc):
    if sort_type == "ten":
        sts_list.sort(key=lambda x: x["ten"], reverse=not isAsc)
    elif sort_type == "diem_tb":
        sts_list.sort(key=lambda x: x["diem_tb"], reverse=not isAsc)


def generate_statistics():
    yeu_count = sum(1 for sts in sts_list if sts["xep_loai"] == "Yếu")
    tb_count = sum(1 for sts in sts_list if sts["xep_loai"] == "Trung Bình")
    kha_count = sum(1 for sts in sts_list if sts["xep_loai"] == "Khá")
    gioi_count = sum(1 for sts in sts_list if sts["xep_loai"] == "Giỏi")
    print("Thống kê điểm TB:")
    print(f"Sinh viên Giỏi: {gioi_count}")
    print(f"Sinh viên Khá: {kha_count}")
    print(f"Sinh viên Trung Bình: {tb_count}")
    print(f"Sinh viên Yếu: {yeu_count}")


def draw_statistics_chart():
    fig, ax = plt.subplots()
    categories = ['Giỏi', 'Khá', 'Trung Bình', 'Yếu']
    counts = [
        sum(1 for sts in sts_list if sts["xep_loai"] == "Giỏi"),
        sum(1 for sts in sts_list if sts["xep_loai"] == "Khá"),
        sum(1 for sts in sts_list if sts["xep_loai"] == "Trung Bình"),
        sum(1 for sts in sts_list if sts["xep_loai"] == "Yếu")
    ]
    ax.bar(categories, counts, color=['green', 'blue', 'orange', 'red'])
    ax.set_xlabel('Xếp loại')
    ax.set_ylabel('Số sinh viên')
    ax.set_title('Biểu đồ thống kê điểm TB')
    plt.show()


def save_to_csv(filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=sts_list[0].keys())
        writer.writeheader()
        writer.writerows(sts_list)


def main():
    menu()
    c = int(input("Chọn chức năng (1-10): "))
    choice(c)


def choice(c):
    match c:
        case 1:
            show_all_students()
        case 2:
            add_students()
        case 3:
            search_id = input("Nhập ID sinh viên cần cập nhật: ")
            update_students(search_id)
        case 4:
            del_id = input("Nhập ID sinh viên cần xóa: ")
            del_students(del_id)
        case 5:
            keyword = input("Nhập từ khóa tìm kiếm (tên hoặc ID): ")
            search_students(keyword)
        case 6:
            sort_choice = sort_menu()
            match sort_choice:
                case 1:
                    sort_students("ten", True)
                case 2:
                    sort_students("ten", False)
                case 3:
                    sort_students("diem_tb", True)
                case 4:
                    sort_students("diem_tb", False)
                case 5:
                    main()
                case _:
                    print("Lựa chọn không hợp lệ. Quay lại menu chính.")
                    main()
        case 7:
            generate_statistics()
        case 8:
            draw_statistics_chart()
        case 9:
            save_to_csv("students.csv")
            print("Lưu danh sách sinh viên vào file students.csv thành công.")
        case 10:
            print("Thoát chương trình.")
            exit()
        case _:
            print("Chức năng không hợp lệ. Vui lòng chọn lại.")
            main()

    main()


main()