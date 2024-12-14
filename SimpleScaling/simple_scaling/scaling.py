import math
import os

import numpy as np
from PIL import Image


def get_img_shape_with_path(img_path):
    img = np.array(Image.open(img_path))
    source_height, source_width, _ = img.shape
    return source_height, source_width, img


def nn_interp(img_path, target_height, target_width):
    img_name = img_path.split("\\")[-1]
    string, ext = os.path.splitext(img_path)
    source_height, source_width, img = get_img_shape_with_path(img_path)
    return_img = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    for i in range(target_height):
        for j in range(target_width):
            source_x = round(i * (source_height / target_height))
            source_y = round(j * (source_width / target_width))
            source_x = min(source_x, source_height - 1)
            source_y = min(source_y, source_width - 1)
            return_img[i, j] = img[source_x, source_y]
    return_img = Image.fromarray(return_img.astype('uint8')).convert('RGB')
    print(img_name + 'has been processed with nn_interp')
    return return_img, ext


def bilinear_interp(img_path, target_height, target_width):
    img_name = img_path.split("\\")[-1]
    string, ext = os.path.splitext(img_path)
    source_height, source_width, img = get_img_shape_with_path(img_path)
    img = np.pad(img, ((0, 1), (0, 1), (0, 0)), 'constant')
    return_img = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    for i in range(target_height):
        for j in range(target_width):
            source_x = i * (source_height - 1) / (target_height - 1)
            source_y = j * (source_width - 1) / (target_width - 1)
            x = math.floor(source_x)
            y = math.floor(source_y)
            u = source_x - x
            v = source_y - y
            return_img[i, j] = (1 - u) * (1 - v) * img[x, y] + u * (1 - v) * img[x + 1, y] + (1 - u) * v * img[
                x, y + 1] + u * v * img[x + 1, y + 1]
    return_img = Image.fromarray(return_img.astype('uint8')).convert('RGB')
    print(img_name + 'has been processed with bilinear_interp')
    return return_img, ext


def bicubic(x, a):
    if (abs(x) >= 0) & (abs(x) <= 1):
        return (a + 2) * (abs(x) ** 3) - (a + 3) * (abs(x) ** 2) + 1

    elif (abs(x) > 1) & (abs(x) <= 2):
        return a * (abs(x) ** 3) - (5 * a) * (abs(x) ** 2) + (8 * a) * abs(x) - 4 * a
    return 0


def padding(img, H, W, C):
    zimg = np.zeros((H + 4, W + 4, C))
    zimg[2:H + 2, 2:W + 2, :C] = img
    zimg[2:H + 2, 0:2, :C] = img[:, 0:1, :C]
    zimg[H + 2:H + 4, 2:W + 2, :] = img[H - 1:H, :, :]
    zimg[2:H + 2, W + 2:W + 4, :] = img[:, W - 1:W, :]
    zimg[0:2, 2:W + 2, :C] = img[0:1, :, :C]
    zimg[0:2, 0:2, :C] = img[0, 0, :C]
    zimg[H + 2:H + 4, 0:2, :C] = img[H - 1, 0, :C]
    zimg[H + 2:H + 4, W + 2:W + 4, :C] = img[H - 1, W - 1, :C]
    zimg[0:2, W + 2:W + 4, :C] = img[0, W - 1, :C]
    return zimg


def bicubic_interp(img_path, target_height, target_width):
    img_name = img_path.split("\\")[-1]
    string, ext = os.path.splitext(img_path)
    a = -1
    img = np.array(Image.open(img_path))
    source_height, source_width, colors = img.shape
    h = source_height / target_height
    img = padding(img, source_height, source_width, colors)
    return_img = np.zeros((target_height, target_width, 3))
    for c in range(colors):
        for j in range(target_height):
            for i in range(target_width):
                x, y = i * h + 2, j * h + 2
                x1 = 1 + x - math.floor(x)
                x2 = x - math.floor(x)
                x3 = math.floor(x) + 1 - x
                x4 = math.floor(x) + 2 - x
                y1 = 1 + y - math.floor(y)
                y2 = y - math.floor(y)
                y3 = math.floor(y) + 1 - y
                y4 = math.floor(y) + 2 - y
                mat_l = np.matrix([[bicubic(x1, a), bicubic(x2, a), bicubic(x3, a),
                                    bicubic(x4, a)]])
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
                    [[bicubic(y1, a)], [bicubic(y2, a)], [bicubic(y3, a)], [bicubic(y4, a)]])
                return_img[j, i, c] = np.dot(np.dot(mat_l, mat_m), mat_r)
    return_img = Image.fromarray(return_img.astype('uint8')).convert('RGB')
    print(img_name + ' has been processed with bicubic_interp')
    return return_img, ext



