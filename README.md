<h2>该项目用于增强超分辨率模型 [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) 的效果</h2>
<h4>仅用于记录个人毕设，仅供学习参考</h4>
和原版Real-ESRGAN相比最大的区别在于引入了真实退化的数据（俗称电子包浆）对原模型进行强化，效果请参考 [文档](./doc.pdf) <br>
如果需要我的数据集，后续可以放上来；但是数据集的量不算大，目前还是采用手工的方式对图片进行电子包浆
<br>
<h3>使用顺序</h3>

<h4>1. [SimpleScaling](SimpleScaling/README.md) / [bicubic](./bicubic/README.md) 生成并处理数据集</h4>
<h4>2. [ORSR](ORSR/README.md) 训练/测试超分辨率模型</h4>
<h4>3. [DeSRA](mmsegmentation/desra/README.md) (在 [mmsegmentation](./mmsegmentation) 内) 检测伪影 （实验中）</h4>
<h4> [mmsegmentation](mmsegmentation/README_zh-CN.md) 为 [DeSRA](./mmsegmentation/desra) 提供必要环境，故一起打包放在这里。</h4>

<h3>具体使用方法请参考各项目内的readme文件以及本目录所附的 [文档](./doc.pdf) </h3>

以后有空的话会全部整理一遍。可以修改的地方还有很多，比如前端UI，自动化的电子包浆之类的。
