<h2>该部分可参考原项目 [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)</h2>
<br>
<h3>快速推理</h3>
<h4>https://github.com/xinntao/Real-ESRGAN/blob/master/README_CN.md</h4>
<h3>训练/微调</h3>
<h4>https://github.com/xinntao/Real-ESRGAN/blob/master/docs/Training_CN.md</h4>
<h3>伪影检测</h3>
<h4>https://github.com/TencentARC/DeSRA</h4>
<br>

<h2>使用流程</h2>

<h3>1. 预训练前的准备</h3>
<font size='2'>首先准备好你的数据集。标准的Real-ESRGAN数据集收集请参考原项目的 ["训练/微调"](https://github.com/xinntao/Real-ESRGAN/blob/master/docs/Training_CN.md) 部分

例如可下载DIV2K数据集 http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_HR.zip

或者Flickr2K数据集 https://cv.snu.ac.kr/research/EDSR/Flickr2K.tar

整理好后将它们放在 [./datasets/train/train_HR](./datasets/train/train_HR) 目录下

随后使用 
`python scripts/generate_multiscale.py --input datasets/train/train_HR --output datasets/train/train_multiscale`
生成多尺寸图片

再使用`python scripts/extract_subimages.py --input datasets/train/train_multiscale --output datasets/train/train_multiscale_sub --crop_size 400 --step 200
`进一步将其裁剪为子图像从而加快处理速度

最后使用`python scripts/generate_meta_info.py --input datasets/train/train_multiscale_sub --meta_info datasets/train/meta_info/meta_info_train.txt` 生成元信息
</font>

<h3>2. 预训练 Real-ESRNET 模型</h3>
<font size='2'>下载预训练模型 [ESRGAN](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/ESRGAN_SRx4_DF2KOST_official-ff704c30.pth) 放在 [experiments/pretrained_models](experiments/pretrained_models) 目录下

检查 [train_orsrnet_x4.yml](options/train_orsrnet_x4.yml) 中的参数，如果前面路径都没有变的话，这一步可以跳过

进行预训练`python orsr/train.py opt options/train_orsrnet_x4.yml --auto_resume`

预训练结束后，得到 [experiments/train_orsrnet_x4/models/net_g_latest.pth](experiments/train_orsrnet_x4/models/net_g_latest.pth) ，将其作为下一步训练的pretrain模型，并复制到 [weights](weights) 目录下，粘贴为 [weights/orsrnet_x4.pth](weights/orsrnet_x4.pth)

<h3>3. 训练 Real-ESRGAN 模型</h3>
<font size='2'>如有需要可检查配置文件 [options/train_orsrgan_x4.yml](options/train_orsrgan_x4.yml) （按照我的路径来的话，应该不需要修改配置文件，唯一可能需要修改的是迭代次数，这个根据自身设备情况来）

然后运行`python orsr/train.py -opt options/train_orsrgan_x4.yml --auto_resume` ，你会分别得到生成器 [experiments/train_orsrgan_x4/models/net_g_latest.pth](experiments/train_orsrgan_x4/models/net_g_latest.pth) 和鉴别器 [experiments/train_orsrgan_x4/models/net_g_latest.pth](experiments/train_orsrgan_x4/models/net_g_latest.pth)

把 [生成器](experiments/train_orsrgan_x4/models/net_g_latest.pth) 复制到 [weights](weights) 目录下，粘贴为 [weights/orsrgan_x4.pth](weights/orsrgan_x4.pth)
</font>

<h3>4. 微调</h3>
<font size='2'>首先要建立已配对的数据集，具体过程请参考 [SimpleScaling](../SimpleScaling/README.md) 和 [文档](../doc.pdf) 

将配对好的数据分别放入 [datasets/finetune_pairdata/gt/gt](datasets/finetune_pairdata/gt/gt) 和 [datasets/finetune_pairdata/lq/lq](datasets/finetune_pairdata/lq/lq) 中

随后运行`python scripts/generate_meta_info_pairdata.py --input datasets/finetune_pairdata/gt/gt datasets/finetune_pairdata/lq/lq --meta_info datasets/finetune_pairdata/meta_info/meta_info_pair.txt`
生成元信息

检查 [options/finetune_orsrgan_x4_pairdata.yml](options/finetune_orsrgan_x4_pairdata.yml) 后，即可进行微调训练`python orsr/train.py -opt options/finetune_orsrgan_x4_pairdata.yml --auto_resume`

最终得到的 [experiments/finetune_orsrgan_x4_pairdata/models/net_g_latest.pth](experiments/finetune_orsrgan_x4_pairdata/models/net_g_latest.pth) 即为我们所需的强化模型，可直接用于推理

将其复制粘贴到 [weights/finetune_orsrgan_x4.pth](weights/finetune_orsrgan_x4.pth)
</font>

<h3>5. 推理</h3>
<font size='2'>前面训练的三个模型都可以用于推理；例如，使用 [强化模型](weights/finetune_orsrgan_x4.pth) 推理，先将测试图片放入 [inputs](inputs) 文件夹，再运行`python inference.py -n finetune_orsrgan_x4 -i inputs` ，输出在 [results](results) 文件夹中
</font>

<h3>6. 性能评价指标 </h3>
<font size='2'>计算各方法的超分辨率性能，请使用 [scripts/calculate_loss.py](scripts/calculate_loss.py) ，该脚本能计算超分后的图像，相对原图像的L1损失、L2损失、峰值信噪比和多尺度结构相似性。修改脚本的输入路径后，直接运行即可输出 .txt 文件。
</font>
