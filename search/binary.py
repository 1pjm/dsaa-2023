def binary_search_recursive(array, element, low, high):
    
    if high >= low:
        mid = (high + low) // 2
        print(array[mid])

        if array[mid] == element:
            return mid
        elif array[mid] > element:
            return binary_search_recursive(array, element, low, mid-1)
        else:
            return binary_search_recursive(array, element, mid+1, high)
        
    else:
        return -1
    
from random import randint

arr = []
for _ in range(10):
    arr.append(randint(1, 100))
arr.sort()

N = len(arr)
start = 0
target = arr[randint(1, N)]

print(arr)
print(target)

value = binary_search_recursive(arr, start, N-1, target)
print(value)
