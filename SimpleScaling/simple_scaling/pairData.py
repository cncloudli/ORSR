import os
import math

from PIL.ImageOps import crop

from simple_scaling import scaling
from PIL import Image


def crop_divide_by_4(original_folder, output_folder):
    for img_name in sorted(os.listdir(original_folder)):
        gt_path = os.path.join(original_folder, img_name)
        gt_h, gt_w, img = scaling.get_img_shape_with_path(gt_path)
        # cut the input ground truth pictures to make the sizes of them can be divided by 4
        # after resizing lq pictures, the paired datasets can be used for training
        # you can change this number to what you need
        target_h = math.floor(gt_h / 4) * 4
        target_w = math.floor(gt_w / 4) * 4
        return_img = Image.fromarray(img).convert('RGB').crop((0, 0, target_w, target_h))
        output_path = os.path.join(output_folder, img_name)
        return_img.save(output_path)


def resize_pairdata(lq_folder, gt_folder, output_folder):
    for img_name in sorted(os.listdir(lq_folder)):
        lq_path = os.path.join(lq_folder, img_name)
        gt_path = os.path.join(gt_folder, img_name)
        gt_h, gt_w, _ = scaling.get_img_shape_with_path(gt_path)
        target_h = round(gt_h / 4)
        target_w = round(gt_w / 4)
        return_img, _ = scaling.nn_interp(lq_path, target_h, target_w)
        output_path = os.path.join(output_folder, img_name)
        return_img.save(output_path)
