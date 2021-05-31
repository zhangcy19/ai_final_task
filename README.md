# ai_final_task
*小组成员： 尧廷松、张朝阳、张颢继*


#### 项目说明
+ 项目功能：利用AI实现合成大西瓜
+ 项目包括：游戏源码，图像识别程序，游戏算法（启发式+强化学习），移动端脚本程序
+ 使用说明：
  1. 安装相关库。提供requirements，可以快速安装环境
  	```bash
  	pip3 install -r requirements.txt
  	```
  	
  2. 运行游戏。若想在本地实现可参考 [*该教程*](https://mp.weixin.qq.com/s/H9VR1MWn-9bKSC_1l_MkJw)，本文件已提供游戏程序，并进行了必要改造
  3. 运行项目。提供makefile，可以分别运行三种算法，初次运行程序会要求提供浏览器文件下载地址（用于游戏分数的输出）以及框选游戏屏幕区域(用于图像识别)，以后不再需要
  4. windows系统需要将通过os.system()函数调用的命令行语句改为windows格式
  > 如果想强制重新初始化，请将assist_data/state.txt内的1改为0
  
  > 如果不希望生成过程记录，请添加 *-off* 选项

  > 如果想要看到实时渲染情况，请添加 *-video* 选项
  
  > 具体使用见Makefile 

#### 进展情况
+ ~~接口实现~~ 
+ 启发式算法
+ 强化学习算法
+ 封装



#### 版权声明
+ 游戏源码源自网友 [*程序员鱼皮*](https://mp.weixin.qq.com/s/H9VR1MWn-9bKSC_1l_MkJw) 并进行了修改（去除广告，打开获取得分的接口）
+ 图像识别基于百度开源深度学习平台 [*paddlex*](https://www.paddlepaddle.org.cn) 进行模型训练与优化，游戏算法使用了python的 [*sklearn库*](https://scikit-learn.org/stable/) 









