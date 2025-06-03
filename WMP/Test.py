# list = [3, 54, 67, 40]
#print(list.reverse)

# print(list[::-1])

def rev_str(str):
    return str[::-1]
    # res = my_list[::-1].join("")
    # return res

def count_letter(str):
    for i in range(len(str)):
        # print("Letter",i,str[i])
        print("count of",str[i],str.count(str[i]))

my_str = "NITIN"

count_letter(my_str)

# if my_str == rev_str(my_str):
#     print(my_str,"is palindrome")
# else:
#     print(my_str,"is not palindrome")    

# print(reverse(list))

# [40, 67, 54, 3]