import cv2
import numpy as np
# filename='original.png'
filename='noise.png'
img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
cv2.namedWindow('main')
cv2.imshow('main',img)
cv2.waitKey(0)

#  MEDIAN_FILTER TO REMOVE NOISE FROM IMG

def median_filter(noise_img):
    final = noise_img[:]
    for y in range(len(noise_img)):
        for x in range(y):
            final[y, x] = noise_img[y, x]
    kernel = [noise_img[0, 0]] * 9
    for y in range(1, len(noise_img) - 1):
        for x in range(1, noise_img.shape[1] - 1):
            kernel[0] = noise_img[y - 1, x - 1]
            kernel[1] = noise_img[y, x - 1]
            kernel[2] = noise_img[y + 1, x - 1]
            kernel[3] = noise_img[y - 1, x]
            kernel[4] = noise_img[y, x]
            kernel[5] = noise_img[y + 1, x]
            kernel[6] = noise_img[y - 1, x + 1]
            kernel[7] = noise_img[y, x + 1]
            kernel[8] = noise_img[y + 1, x + 1]

            kernel.sort()
            final[y, x] = kernel[4]
    return final


blur_img=median_filter(img)
cv2.namedWindow('main2')
cv2.imshow('main2', blur_img)  # FINAL=IMG WITHOUT NOISE
cv2.waitKey(0)
# blur_img=cv2.imwrite('C:/Users/Roumk/OneDrive/Υπολογιστής/HW_1', blur_img)

# CONVERT BLUR_IMG TO BINARY
ret,thresh_img = cv2.threshold(blur_img, 20, 255, cv2.THRESH_BINARY)

# VIEW BINARY IMG
cv2.imshow('threshold',thresh_img)
cv2.waitKey(0)

# FUNCTION THAT FINDS INTEGRAL
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





# FUNCTION TO RETURN FINAL_IMG
def connected_components(new_img):
    final_img = cv2.cvtColor(blur_img, cv2.COLOR_GRAY2BGR)
    item = my_integral(blur_img)
    output = cv2.connectedComponentsWithStats(thresh_img, 8, cv2.CV_32S)
    num_labels = output[0] # The first cell is the number of labels
    labels = output[1]     # The second cell is the label matrix
    values = output[2]     # The third cell is the stat matrix
    centroids = output[3]  # The fourth cell is the centroid matrix
    j=0   # initialize counter
    for i in range(1,num_labels):
        area=values[i,cv2.CC_STAT_AREA]

        if area>10:
           j=j+1  # counter
           x1 = values[i, cv2.CC_STAT_LEFT]
           y1 = values[i, cv2.CC_STAT_TOP]
           w = values[i, cv2.CC_STAT_WIDTH]
           h = values[i, cv2.CC_STAT_HEIGHT]

           # CORDINATE FOR BOUNDING BOX
           pt1 = (x1, y1)
           pt2 = (x1 + w, y1 + h)
           (X, Y) = centroids[i]
           box_sum=integral_sum(item,y1,x1,y1+h,x1+w)
           average=box_sum/(w*h)
           # BOUNDING BOXES FOR EACH ELEMENT
           color=(0,0,255)
           cv2.rectangle(final_img, pt1, pt2, color, 1)
           # PUT TEXT IN IMG

           # font = cv2.FONT_HERSHEY_SIMPLEX
           font = cv2.FONT_HERSHEY_COMPLEX_SMALL
           org = (x1,y1+int(h/2))
           fontScale=1
           color=(0,0,255)
           thickness=1
           new_img = cv2.putText(final_img, str(j), org, font, fontScale, color, thickness, cv2.LINE_AA)
           # PRINTS
           print(f'----Region'f'{j} : ----')
           print(f'Area(px)'f':', area)
           print(f'Bounding Box Area(px)'f' :', w * h)
           print(f'Mean graylevel value in bounding box 'f' :', average)
    return new_img

final_img=connected_components(thresh_img)
cv2.imshow('final_img',final_img )
cv2.waitKey(0)
por=cv2.imwrite('noise_final_img.png',final_img)
print(por)


