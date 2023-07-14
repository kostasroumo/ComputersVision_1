def my_integral(image):
    N = len(image)
    M = len(image[0])
    array_of_sums = np.empty([N, M], dtype=int)

    for i in range(0, N, 1):
        sum = 0
        for j in range(0, M, 1):
            sum = image[i][j] + sum
            array_of_sums[i][j] = sum

    for i in range(1, N, 1):
        for j in range(M-1, -1, -1):
            array_of_sums[i][j] += array_of_sums[i - 1][j]

    col = np.array([np.zeros(N + 1)])
    row = np.array([np.zeros(M)])
    row_arr = np.insert(array_of_sums, 0, row, axis=0)
    final_arr = np.insert(row_arr, 0, col, axis=1)

    return final_arr


def integral_sum(new_array,si,sj,ei,ej):
    sum = new_array[ei, ej] - new_array[ei, sj] - new_array[si, ej] + new_array[si, sj]
    return sum