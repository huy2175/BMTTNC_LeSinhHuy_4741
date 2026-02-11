def dao_nguoc_list(lst):
    return lst[::-1]

input_list = input("Nhập danh sách các số, cách nhau bằng dấu phẩy: ")
numbers = list(map(int, input_list.split(',')))
print("List sau khi đảo ngược:", dao_nguoc_list(numbers))