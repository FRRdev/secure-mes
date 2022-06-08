from collections import Counter


def find_uniq(arr):
    c = Counter(arr)
    for key, value in c.items():
        if value == 1:
            return key


# import re
#
# pattern_for_duplicate = re.compile('\d+')
# arr = re.findall(pattern_for_duplicate, '150000000 рублей внесу')
# if len(arr) != len(set(arr)):
#     sum_str = arr[0]
# else:
#     find_digits = re.compile('\d')
#     list_all_digits = re.findall(find_digits, '150000000')
#     sum_str = ''.join(list_all_digits)
# print(sum_str)


def custom_generator(seq):
    for i in range(len(seq)):
        yield seq[i]
    for _ in range(3):
        yield -1


import re

pattern_for_duplicate = re.compile('\d+')
arr = re.findall(pattern_for_duplicate, '15224 рубля 59 копеек если я запомнила верно')
print(arr)
if len(arr) != len(set(arr)):
    sum_str = arr[0]
else:
    find_digits = re.compile('\d')
    list_all_digits = re.findall(find_digits, '15224 рубля 59 копеек если я запомнила верно')
    sum_str = ''.join(list_all_digits)
    if 'коп' in '15224 рубля 59 копеек если я запомнила верно':
        sum_str = sum_str[:-2]

print(sum_str)
