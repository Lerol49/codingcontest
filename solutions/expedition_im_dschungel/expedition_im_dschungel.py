import math



tempel = (4, 3)

def street(x):
    return 2 / 7 * x

def dist_to_tempel(x):
    return math.sqrt((x - tempel[0]) ** 2 + (street(x) - tempel[1]) ** 2)


left = 0
right = 10
for i in range(29):  # this is actually enough
    if dist_to_tempel(left) < dist_to_tempel(right):
        right -= 0.5 * (right - left)
    elif dist_to_tempel(left) > dist_to_tempel(right):
        left += 0.5 * (right - left)


    # print("left: ", left)
    # print("right:", right)
    # print("dist_left: ", dist_to_tempel(left))
    # print("dist_right:", dist_to_tempel(right))


answer = (left + right) / 2
print(answer)

# 4.490566048771143     output
# 4.490566037735849     expected


