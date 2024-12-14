import cv2
import numpy as np
import math
import sys, time

#双三次插值脚本
def u(s, a):
    if (abs(s) >= 0) & (abs(s) <= 1):
        return (a + 2) * (abs(s) ** 3) - (a + 3) * (abs(s) ** 2) + 1

    elif (abs(s) > 1) & (abs(s) <= 2):
        return a * (abs(s) ** 3) - (5 * a) * (abs(s) ** 2) + (8 * a) * abs(s) - 4 * a
    return 0


def padding(img, H, W, C):
    zimg = np.zeros((H + 4, W + 4, C))
    zimg[2:H + 2, 2:W + 2, :C] = img

    # Pad the first/last two col and row
    zimg[2:H + 2, 0:2, :C] = img[:, 0:1, :C]
    zimg[H + 2:H + 4, 2:W + 2, :] = img[H - 1:H, :, :]
    zimg[2:H + 2, W + 2:W + 4, :] = img[:, W - 1:W, :]
    zimg[0:2, 2:W + 2, :C] = img[0:1, :, :C]

    # Pad the missing eight points
    zimg[0:2, 0:2, :C] = img[0, 0, :C]
    zimg[H + 2:H + 4, 0:2, :C] = img[H - 1, 0, :C]
    zimg[H + 2:H + 4, W + 2:W + 4, :C] = img[H - 1, W - 1, :C]
    zimg[0:2, W + 2:W + 4, :C] = img[0, W - 1, :C]

    return zimg


def bicubic(img, ratio, a):
    # Get image size
    H, W, C = img.shape

    img = padding(img, H, W, C)

    # Create new image
    dH = math.floor(H * ratio)
    dW = math.floor(W * ratio)

    # Converting into matrix
    dst = np.zeros((dH, dW, 3))

    # np.zeroes generates a matrix
    # consisting only of zeroes
    # Here we initialize our answer
    # (dst) as zero

    h = 1 / ratio

    print('Start bicubic interpolation')
    print('It will take a little while...')
    inc = 0

    for c in range(C):
        for j in range(dH):
            for i in range(dW):
                # Getting the coordinates of the
                # nearby values
                x, y = i * h + 2, j * h + 2

                x1 = 1 + x - math.floor(x)
                x2 = x - math.floor(x)
                x3 = math.floor(x) + 1 - x
                x4 = math.floor(x) + 2 - x

                y1 = 1 + y - math.floor(y)
                y2 = y - math.floor(y)
                y3 = math.floor(y) + 1 - y
                y4 = math.floor(y) + 2 - y

                # Considering all nearby 16 values
                mat_l = np.matrix([[u(x1, a), u(x2, a), u(x3, a), u(x4, a)]])
                mat_m = np.matrix([[img[int(y - y1), int(x - x1), c],
                                    img[int(y - y2), int(x - x1), c],
                                    img[int(y + y3), int(x - x1), c],
                                    img[int(y + y4), int(x - x1), c]],
                                   [img[int(y - y1), int(x - x2), c],
                                    img[int(y - y2), int(x - x2), c],
                                    img[int(y + y3), int(x - x2), c],
                                    img[int(y + y4), int(x - x2), c]],
                                   [img[int(y - y1), int(x + x3), c],
                                    img[int(y - y2), int(x + x3), c],
                                    img[int(y + y3), int(x + x3), c],
                                    img[int(y + y4), int(x + x3), c]],
                                   [img[int(y - y1), int(x + x4), c],
                                    img[int(y - y2), int(x + x4), c],
                                    img[int(y + y3), int(x + x4), c],
                                    img[int(y + y4), int(x + x4), c]]])
                mat_r = np.matrix(
                    [[u(y1, a)], [u(y2, a)], [u(y3, a)], [u(y4, a)]])

                dst[j, i, c] = np.dot(np.dot(mat_l, mat_m), mat_r)

    sys.stderr.write('\n')

    sys.stderr.flush()
    return dst

#测试用，直接生成bicubic插值后的结果，可以按需求注释掉
img = cv2.imread('test1.jpg')
ratio = 4
a = -1
dst = bicubic(img, ratio, a)
print('Completed!')
cv2.imwrite('test1_bicubic.jpg', dst)

img = cv2.imread('test10.jpg')
ratio = 4
a = -1
dst = bicubic(img, ratio, a)
print('Completed!')
cv2.imwrite('test10_bicubic.jpg', dst)

img = cv2.imread('test5.jpg')
ratio = 4
a = -1
dst = bicubic(img, ratio, a)
print('Completed!')
cv2.imwrite('test5_bicubic.jpg', dst)

img = cv2.imread('test6.jpg')
ratio = 4
a = -1
dst = bicubic(img, ratio, a)
print('Completed!')
cv2.imwrite('test6_bicubic.jpg', dst)

img = cv2.imread('test7.jpg')
ratio = 4
a = -1
dst = bicubic(img, ratio, a)
print('Completed!')
cv2.imwrite('test7_bicubic.jpg', dst)

img = cv2.imread('test8.jpg')
ratio = 4
a = -1
dst = bicubic(img, ratio, a)
print('Completed!')
cv2.imwrite('test8_bicubic.jpg', dst)

img = cv2.imread('test9.jpg')
ratio = 4
a = -1
dst = bicubic(img, ratio, a)
print('Completed!')
cv2.imwrite('test9_bicubic.jpg', dst)