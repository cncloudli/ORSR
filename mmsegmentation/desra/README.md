<h3> 伪影检测（实验性）</h3>

此项为实验性功能，不能保证其结果的正确性。[DeSRA](https://github.com/TencentARC/DeSRA) 的原理大致是：为了检测GAN网络（此处为Real-ESRGAN及其强化网络）的特有伪影，可尝试利用不含判别器的对应网络（此处为Real-ESRNet）的超分结果，与GAN网络的SR结果进行比对。

将Real-ESRGAN的SR结果放入 [desra/artifact_datasets/gan](desra/artifact_datasets/gan) ，Real-ESRNet的SR结果放入 [desra/artifact_datasets/mse](desra/artifact_datasets/mse) ，然后运行`python desra/scripts/artifact_detection.py --mse_root="desra/artifact_datasets/mse" --gan_root="desra/artifact_datasets/gan" --save_root="desra/outputs"` 即可生成伪影图