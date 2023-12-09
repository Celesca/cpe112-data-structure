my_list = [
    [0.99539, -0.05889, 0.85243, 0.02306, 0.83398, -0.37708, 1, 0.0376, 0.85243, -0.17755, 0.59755, -0.44945, 0.60536, -0.38223, 0.84356, -0.38542, 0.58212, -0.32192, 0.56971, -0.29674, 0.36946, -0.47357, 0.56811, -0.51171, 0.41078, -0.46168, 0.21266, -0.3409, 0.42267, -0.54487, 0.18641, -0.453, 'g'],
    [1, -0.18829, 0.93035, -0.36156, -0.10868, -0.93597, 1, -0.04549, 0.50874, -0.67743, 0.34432, -0.69707, -0.51685, -0.97515, 0.05499, -0.62237, 0.33109, -1, -0.13151, -0.453, -0.18056, -0.35734, -0.20332, -0.26569, -0.20468, -0.18401, -0.1904, -0.11593, -0.16626, -0.06288, -0.13738, -0.02447, 'b'],
    [0.99539, -0.05889, 0.85243, 0.02306, 0.83398, -0.37708, 1, 0.0376, 0.85243, -0.17755, 0.59755, -0.44945, 0.60536, -0.38223, 0.84356, -0.38542, 0.58212, -0.32192, 0.56971, -0.29674, 0.36946, -0.47357, 0.56811, -0.51171, 0.41078, -0.46168, 0.21266, -0.3409, 0.42267, -0.54487, 0.18641, -0.453, 'g']
]

sorted_list = sorted(my_list, key=lambda x: x[-1])  # Sorting based on the last element of each sub-list

print(sorted_list)