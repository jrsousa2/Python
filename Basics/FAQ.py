# ========== COLUMN 1 ==========

# 1. Check if list contains integer x
lst = [3, 3, 4, 5, 2, 111, 5]
print("Q1 check if number is in list",111 in lst)  # True

# 2. Find duplicate number in integer list
def find_duplicates(elements):
    duplicates, seen = set(), set()
    for element in elements:
        if element in seen:
            duplicates.add(element)
        seen.add(element)
    return list(duplicates)

print("Q2 Dupes:",find_duplicates(lst))

# 3. Check if two strings are anagrams
def is_anagram(s1, s2):
    return sorted(s1) == sorted(s2)

print("Q3 are 2 words anagrams", is_anagram("elvis", "lives"))  # True

# 4. Remove all duplicates from list
lst = list(range(10)) + list(range(10))
lst = list(set(lst))

print("Q4 removes dupes from list with set",lst)  # Output: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 5. Find pairs of integers in list so that their sum is equal to integer x
def find_pairs(lst, x):
    pairs = []
    for (i, el_1) in enumerate(lst):
        for (j, el_2) in enumerate(lst[i + 1:]):
            if el_1 + el_2 == x:
                pairs.append((el_1, el_2))
    return pairs

print("Q5 the pairs that sum to",9,"are",find_pairs(lst, 9))  # Output: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


# THIS IS WRONG
lst = list(range(10)) + list(range(10))
lst = list(set(lst))

print("Q5",lst)  # Output: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 6. Check if a string is a palindrome


# 7. Use list as stack, array, queue
# As stack
stack = [3, 4, 5]
stack.append(6)
stack.append(7)
print(stack)  # Output: [3, 4, 5, 6, 7]
stack.pop()
print(stack)  # Output: [3, 4, 5, 6]

# As queue
queue = [3, 4, 5, 6]
queue.pop(0)
print(queue)  # Output: [4, 5, 6]

# ========== COLUMN 2 ==========

# 8. Get missing number in [1...100]
# THE BELOW IS WRONG
def get_missing_number(lst):
    return set(range(1, lst[len(lst) - 1])) - set(lst)

# NOTE THE BELOW IS THE DIFFERENCE
def get_missing_numbers(lst):
    return sorted(set(range(1, 101)) - set(lst))

print("Q8",)

lst = list(range(1, 100))
lst.remove(50)
print(get_missing_number(lst))  # Output: {50}

# 9. Compute the intersection of two lists
def intersect(lst1, lst2):
    lst2_copy = lst2[:]
    res = []
    for el in lst1:
        if el in lst2_copy:
            res.append(el)
            lst2_copy.remove(el)
    return res

# 10. Find max and min in unsorted list
lst = [4, 3, 6, 4, 888, 1, -11, 22, 3]
print(max(lst))  # Output: 888
print(min(lst))  # Output: -11

# 11. Reverse string using recursion
def reverse(string):
    if len(string) <= 1:
        return string
    return reverse(string[1:]) + string[0]

print(reverse("hello"))  # Output: olleh

# 12. Compute the first n Fibonacci numbers
a, b = 0, 1  # initialize the first two
n = 10
for i in range(n):
    print(a)
    a, b = b, a + b

# 13. Sort list with Quicksort algorithm
def qsort(l):
    if len(l) <= 1:
        return l
    return qsort([x for x in l[1:] if x < l[0]]) + [l[0]] + qsort([x for x in l[1:] if x >= l[0]])

lst = [44, 33, 22, 55, 77, 999]
print(qsort(lst))  # Output: [22, 33, 44, 55, 77, 999]

# 14. Find all permutations of string
def get_permutations(w):
    if len(w) <= 1:
        return set(w)
    smaller = get_permutations(w[1:])
    perms = set()
    for x in smaller:
        for pos in range(len(w)):
            perms.add(x[:pos] + w[0] + x[pos:])
    return perms

print(get_permutations("ann"))
# Output: {'ann', 'nan', 'nna'}
