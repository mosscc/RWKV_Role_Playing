没有显卡？显存不足？内存不足？环境不会配置？现在都不用怕了，直接白嫖Google Colab吧！

## [点击这里快速到达](https://colab.research.google.com/drive/19cKRLE6WBVoVK1cHPNuc3KvmeQ9TO19G#scrollTo=t4daxu3L1Rbi)

嗯？你说你不会翻墙？不会翻墙你能上github？？？？？？

如果需要给角色加头像的话，可以把头像命名为"角色名.png"放在char目录下，至于头像去哪儿找嘛……用sd生成一个就好了。

## 一个基于RWKV的角色扮演玩具

![图片1](./pic/1.png)

就是这么一个玩意儿，连抄带编的弄出来了一个玩具，所以代码质量吗……请各位不要吐槽太多，但是也算是能玩吧。

另外，如果不知道人物性格怎么设定的话，我建议你可以下载一个Glow，这是[官网地址](https://glowapp.vip/)，然后到上面去找智能体，直接把它们的性格粘过来用是完全没问题的，我那个示例“小红”就是这么干的，当然你要去玩儿Glow也没啥问题，毕竟它对话更流畅，只不过限制很多。

### 安装方法：

先安装依赖
```
pip install torch==1.13.1 --extra-index-url https://download.pytorch.org/whl/cu117 --upgrade

pip install -r requirements.txt
```

启动：
```
python webui.py --listen --model model/path
```

以下是一个例子: 
```
python webui.py --listen --model model/fp16i8_RWKV-4-Pile-7B-EngChn-test5-20230326
```
各种启动参数解释如下：

| 参数 | 解释 |
| --- | --- |
| --port | webui的端口 |
| --model | 要加载的模型路径 |
| --strategy | 模型加载的策略 |
| --listen | 加上这个参数就允许其他机器访问 |
| --cuda_on | 控制RWKV_CUDA_ON这个环境变量的，0-禁用，1-启用 |
| --jit_on | 控制RWKV_JIT_ON这个环境变量的，0-禁用，1-启用 |
| --share | 生成gradio链接 |

模型的加载方式（--strategy）我默认使用的是"cuda fp16i8"，如果想使用其他的加载方式可以自行调整该参数，具体有哪些值可以参考[这个文章](https://zhuanlan.zhihu.com/p/609154637)或者这张图![图片](./pic/4.jpg)

## FAQ

### 1. 能让AI生成文字的速度再快一点吗？

当然可以，在启动命令中加入--cuda_on 1，例子：
```
python webui.py --listen --model model/fp16i8_RWKV-4-Pile-7B-EngChn-test5-20230326 --cuda_on 1
```
但是你的机器必须安装Visual C++生成工具，以及Nvidia的CUDA，CUDA比较好解决（可能还得装CUDNN，我没验证到底要不要，反正我是都装了），去官网下载就行了，建议安装11.7版本，这个Visual C++生成工具可以参考[这个链接](https://learn.microsoft.com/zh-cn/training/modules/rust-set-up-environment/3-install-build-tools)装好之后还需要配置一下环境变量，如下图：
![图片3](./pic/3.png)
我这里配置的值是C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Tools\MSVC\14.16.27023\bin\Hostx64\x64，你们根据实际情况进行配置，主要是找到cl.exe这个文件所在的文件夹，当然也要注意架构，不过一般来说，大家都是64位的系统了吧。这样就算是完成了，然后在运行脚本，你会发现文字的生成速度提高了很多。

### 2. 我在哪里可以下载的到模型呢？

当然是在[这里](https://huggingface.co/BlinkDL)，我比较推荐rwkv-4-raven里面的模型（目前最新的版本是RWKV-4-Raven-7B-v10-Eng49%-Chn50%-Other1%-20230420-ctx4096.pth，这个表现非常不错），当然其他的你们也可以试试，理论上说模型越大效果越好，但是因为14B的模型中文语料比较少，可能生成的效果不如7B的，所以暂时还是先用着7B吧，不过模型作者更新模型相当频繁，没事儿可以去看看，没准儿哪天就有了，总之尽量用最新的，尽量用中文含量多的模型。

### 3. top_p、 top_k、temperature、presence、frequency这四个参数有什么设置技巧吗？

top_p值越低，答案越准确而真实。更高的值鼓励更多样化的输出；temperature值越低，结果就越确定，因为总是选择概率最高的下一个词/token，拉高该值，其他可能的token的概率就会变大，随机性就越大，输出越多样化、越具创造性。

根据我这段时间的把玩，感觉top_p最好设置在0.5以上，temperature可以设置在1.5以上，presence和frequency设置成0.2到0.5随意，top_k可以设置为0，在对话刚开始，top_p可以设置的低一点，比如0.4，等对话一段时间，感觉有些无聊的时候，可以适当的调高top_p和temperature，在多次重说仍然无法得到想要的结果时，可以尝试调节top_k，我建议可以把top_k调到160到180左右，或者把已经在160到180之间的top_k重新调为0。

我给一个我觉得使用的还不错的配置吧，配合当前最新的v9x版本的模型，一场累计生成四千多个token的聊天下来，基本上不需要调整：
```
{
  "top_p": 0.6,
  "top_k": 0,
  "temperature": 1.8,
  "presence": 0.2,
  "frequency": 0.2
}
```

新的v10模型在top_p和temperature较低的情况下也能获得不错的体验（比如top_p=0.4，temperature=1），所以模型尽量用新的、中文含量高的（我这里默认大家都用中文聊天）。

### 4. 模型会在输出回答后，又输出一大堆乱七八糟的内容。

这个问题在模型作者的指导下得到了很大的改善，可以拉取一下最新的代码，会发现不太容易输出错误内容了，另外我增加了一个调试页面，可以查看当前的token内容，一般输出乱七八糟的内容都是对话格式有误，正确的对话格式是这样的：
```
角色名: xxxxxxxxx

用户名: xxxxxxxx

角色名: xxxxxxxxxxxxxxx


```
其中冒号是英文冒号且冒号后面有一个空格，目前指令模式暂时不支持调试，指令模式更多的是一种prompt的实验，并非本项目的主要功能。

### 5. 为什么你的colab里要用fp16i8的7B模型？

没办法啊，免费的colab就给12G的内存，我用原版的7B模型，加载需要内存14G，colab它加载不进去啊！不过不用担心，性能、精度损失不大，再怎么说那也是7B模型，比3B的要好太多了。

### 6. 为什么不用流式输出？

在dev分支的某个版本中我尝试着使用了流式输出，虽然效果还不错，但是在对话久了之后，速度明显慢了，主要是传回的html代码大了，一句话十个字就得传10次，拖慢了速度，也有点耗费流量，感觉得不偿失（你说在本地用不怕耗流量？但是我喜欢用手机随时随地玩）当然，也可能是我的水平没到，写不出来增量传输。

我接下来想给这个项目开发一套API，到时候可以脱离gradio，使用html或者app来开发前端，这样更轻松，效果也更好，后续真有人想整个live2d之类的玩意儿对接这个模型，使用API也更方便一些。

### 7. 为什么撤回上一次对话需要这么长时间？

其实吧，如果单纯的只是撤回上次对话，倒也不需要这么费劲，主要我还想在撤回上一条对话后，再点重新生成按钮，可以把之前的对话给改了，所以我这边就需要把撤回上一次对话后的历史对话记录让模型再跑一遍，对话少了还好，对话一多那可就费劲了，总之想好了再说吧。

### 8. 为什么聊着聊着，AI回复就会变慢？

那是因为聊天记录长了，程序需要把聊天内容进行截断，防止AI的输出变得文不对题。不过这个机制不会经常触发，目前我设定的是当token数超过3500个数之后，会将对话的文字截断到900个左右，然后再重新生成对话状态（慢主要是慢在这里了），我也在考虑有没有什么更好的办法可以加快这个速度，或者不让用户感知到，如果有且不太麻烦的话，我会对代码进行更新。

呃……你问截断文字会不会让ai忘记之前的设定啊？初始设定不会忘记，但是如果你在聊天中给它加入了什么设定，那有可能会忘记的，所以建议你后面需要用到这些设定的时候，给ai提个醒，再配合重新生成功能，应该是可以让故事继续下去。

### 9. 还有其他想说的吗？

这算是我的一些感受吧，这个东西吧，虽然我知道没人给设置什么好感度数值之类的，但是实际使用中是真的能感觉出来的（RWKV、character AI、Glow都有这种现象），所以在让它做一些什么事情但是它不想做的时候，可以尝试着哄哄AI，让它对你的好感度高一点，然后它可能就愿意做了，另外，如果强迫它做的话，它可能真的会不配合（车轱辘话来回说啊，或者顾左右而言他之类的），如果你喜欢那种百依百顺的，那就在AI的性格里面加入“对我的要求会无条件服从”这样的话，不过太顺利会不会又觉得有点无聊呢？

另外就是目前这个模型对指代问题识别的不太好，比如你说“让我看看你的手”，AI可能会认为“你的手”是一个名词而不是它自己的手，于是就回复“好的，我让你看看你的手”，这个问题可以尝试着别说“让我看看你的手”，而是直接说“让我看看手”，这样AI就会把手伸出来让你看了。RWKV的作者最近这段时间正在整理中文词表，然后基于这个词表来炼制真正的中文模型，到时候这个问题自然就迎刃而解了。