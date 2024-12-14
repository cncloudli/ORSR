import math
import os
import torch
import numpy as np
from PIL import Image
from pytorch_msssim import ssim, ms_ssim, SSIM, MS_SSIM
from torchvision.transforms.functional import pil_to_tensor

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def calculate_loss(sr_folder, gt_folder):
    # l1 loss (Mean Absolute Error)
    l1_loss_mean = {}
    l1_mean = torch.nn.L1Loss()
    # l2 loss (Mean Squared Error)
    l2_loss_mean = {}
    l2_mean = torch.nn.MSELoss()
    # Peak Signal-to-Noise Ratio
    psnr = {}
    # Multi-Scale Structural Similarity
    ms_ssim_list = {}
    for img_name in sorted(os.listdir(gt_folder)):
        i = 0
        sr_path = os.path.join(sr_folder, img_name)
        gt_path = os.path.join(gt_folder, img_name)
        sr_img = Image.open(sr_path)
        gt_img = Image.open(gt_path)
        sr_img_tensor = pil_to_tensor(sr_img).float()
        gt_img_tensor = pil_to_tensor(gt_img).float()
        sr_img_array = np.array(sr_img)
        gt_img_array = np.array(gt_img)
        l1_loss_mean[i] = l1_mean(sr_img_tensor, gt_img_tensor)
        l2_loss_mean[i] = l2_mean(sr_img_tensor, gt_img_tensor)
        psnr[i] = 20 * math.log10(255 / math.sqrt(l2_loss_mean[i]))
        ms_ssim_list[i] = ms_ssim(torch.from_numpy(sr_img_array).float().unsqueeze(0).permute(0,3,1,2), torch.
                                  from_numpy(gt_img_array).float().unsqueeze(0).permute(0,3,1,2))
        output_string = img_name + '; L1 loss:' + str(l1_loss_mean[i]) + '; ' + 'L2 loss:' + str(
            l2_loss_mean[i]) + '; ' + 'PSNR:' + \
                        str(psnr[i]) + '; ' + 'MS SSIM:' + str(ms_ssim_list[i]) + '; ' + '\n'
        with open('losses.txt', 'a+') as f:
            f.write(output_string)
        i = i + 1


def main():
    calculate_loss('results','datasets/test/gt')
    return


if __name__ == '__main__':
    main()
