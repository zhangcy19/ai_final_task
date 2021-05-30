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
  	
  2. 运行游戏。若想在本地实现可参考 [*该教程*](https://mp.weixin.qq.com/s/H9VR1MWn-9bKSC_1l_MkJw)
  3. 运行项目。提供makefile，可以分别运行三种算法，开始会提示框选游戏屏幕区域，然后开始运算
    ```bash
    make sample
    make heuristic
    make reinforcement
    ```
    >使用 ***uninit*** 选项可以加载已保存的area，不必每次均框选屏幕
    
    >使用 ***image*** 选项可以将过程图片保存至output文件夹
    
    >使用 ***video*** 选项可以实时渲染项目模型
    
    >具体使用见makefile文件
  
    如果使用 ***image*** 选项输出了一系列图片，可以通过以下命令将图片转为GIF
   ```bash
   make save
   ```

#### 进展情况
+ ~~接口实现~~  （还差一个getScore函数用于强化学习>_<）
+ 启发式算法
+ 强化学习算法
+ 封装



#### 版权声明
+ 游戏源码源自网友 [*程序员鱼皮*](https://mp.weixin.qq.com/s/H9VR1MWn-9bKSC_1l_MkJw) 并进行了修改（去除广告、打开部分接口）
+ 图像识别基于百度开源深度学习平台 [*paddlex*](https://www.paddlepaddle.org.cn) 进行模型训练与优化，游戏算法使用了python的 [*sklearn库*](https://scikit-learn.org/stable/) 









