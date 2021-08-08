# ai_final_task
*小组成员： 尧廷松、张朝阳、张颢继*


#### 项目说明
+ 项目功能：利用AI实现合成大西瓜

+ 适用版本：win10，Mac

+ 项目包括：游戏源码，图像识别程序，游戏算法（样例+启发式+机器学习）

+ 使用说明：
  1. 安装相关库。提供requirements，可以快速安装环境
  	```bash
  	pip3 install -r requirements.txt
  	```
  	
  2. 运行游戏。若想在本地实现可参考 [*该教程*](https://mp.weixin.qq.com/s/H9VR1MWn-9bKSC_1l_MkJw)，本文件提供游戏程序支持getScore调试功能，在线使用不支持
  3. 运行项目。可以分别运行三种算法，初次运行程序会要求提供浏览器文件下载地址（用于游戏分数的输出）以及框选游戏屏幕区域(用于图像识别)，以后不再需要。具体使用请见Makefile
  
  	```bash
  	python3 main.py reinforcement(/sample/heuristic)  
  	```
  
  > 如果想要看到实时渲染情况，请添加 *-video* 选项
  
  > 如果不希望生成过程记录，请添加 *-off* 选项

  > 如果想强制初始化，请将assist_data/state.txt内的1改为0

#### 进展情况
+ ~~接口实现~~ 
+ ~~启发式算法~~
+ ~~机器学习算法~~
+ ~~封装~~


#### 版权声明
+ 游戏源码源自网友 [*程序员鱼皮*](https://mp.weixin.qq.com/s/H9VR1MWn-9bKSC_1l_MkJw) 并进行了修改（去除广告，打开获取得分的接口）
+ 图像识别基于百度开源深度学习平台 [*paddlex*](https://www.paddlepaddle.org.cn) 进行模型训练与优化，游戏算法使用了 python 的 pytorch 框架
+ 其余代码均为原创









