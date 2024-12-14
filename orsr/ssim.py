from pytorch_msssim import ssim, ms_ssim, SSIM, MS_SSIM
import numpy as np
import torch
from torchvision.transforms.functional import pil_to_tensor
from PIL import Image
X = np.array(Image.open('datasets/test/orsrgan/test1.jpg'))
Y = np.array(Image.open('datasets/test/gt/test1.jpg'))
X = torch.from_numpy(X).float().unsqueeze(0).unsqueeze(0).permute()/255.0
Y = torch.from_numpy(Y).float().unsqueeze(0).unsqueeze(0).permute()/255.0
# calculate ssim & ms-ssim for each image
ssim_val = ssim( X, Y, data_range=255, size_average=False) # return (N,)
ms_ssim_val = ms_ssim( X, Y, data_range=255, size_average=False ) #(N,)

# set 'size_average=True' to get a scalar value as loss. see tests/tests_loss.py for more details
ssim_loss = 1 - ssim( X, Y, data_range=255, size_average=True) # return a scalar
ms_ssim_loss = 1 - ms_ssim( X, Y, data_range=255, size_average=True )

# reuse the gaussian kernel with SSIM & MS_SSIM.
ssim_module = SSIM(data_range=255, size_average=True, channel=3) # channel=1 for grayscale images
ms_ssim_module = MS_SSIM(data_range=255, size_average=True, channel=3)

ssim_loss = 1 - ssim_module(X, Y)
ms_ssim_loss = 1 - ms_ssim_module(X, Y)