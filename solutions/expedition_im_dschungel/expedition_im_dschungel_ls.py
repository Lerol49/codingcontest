import numpy as np


tempel = (4, 3)

def street(x):
    return 2 / 7 * x

def dist_to_tempel(x):
    return np.sqrt((x - tempel[0]) ** 2 + (street(x) - tempel[1]) ** 2)


def binary_search():
    left = 0
    right = 10
    for i in range(39):  # this is actually enough
        if dist_to_tempel(left) < dist_to_tempel(right):
            right -= 0.5 * (right - left)
        elif dist_to_tempel(left) > dist_to_tempel(right):
            left += 0.5 * (right - left)
    
    
    
    answer = (left + right) / 2
    print(answer, "(output bin search)")


print("4.490566037735849 (expected)")

# 4.490566048771143     output
# 4.490566037735849     expected


