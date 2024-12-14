import os
import simple_scaling.scaling
from PIL import Image

input_folder = 'lq'
nn_output = 'nn_output'
bilinear_output = 'bilinear_output'
bicubic_output = 'bicubic_output'
for img_name in sorted(os.listdir(input_folder)):
    img_path = os.path.join(input_folder, img_name)
    h, w, _ = simple_scaling.scaling.get_img_shape_with_path(img_path)
    nn_return, _ = simple_scaling.scaling.nn_interp(img_path, round(4 * h), round(4 * w))
    nn_return_img = nn_return.save(os.path.join(nn_output, img_name))
    #bilinear_return, _ = simple_scaling.scaling.bilinear_interp(img_path, round(4 * h), round(4 * w))
    #bilinear_return_img = bilinear_return.save(os.path.join(bilinear_output, img_name))

