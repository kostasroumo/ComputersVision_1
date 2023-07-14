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