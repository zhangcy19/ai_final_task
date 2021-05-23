#usage: main.py [init/uninit] [off/image/video] [sample/heuristic/reinforcement]

#[init/uninit]：init会提示框选范围（这个范围会存到area.json中），uinit可以直接加载已有的范围，不再框选
#[off/image/video]：off会关闭可视化，image会把每次判断的结果以图片形式保存到output文件夹，video会调出渲染窗口实时显示模型情况
#[sample/heuristic/reinforcement]：分别对应不同算法

#注意：每个参数都是必须要给的
#写了一些常用的操作方便调试
#可以按照需要自己添加
sample:
	python3 main.py init off sample
heuristic:
	python3 main.py init off heuristic
reinforcement:
	python3 main.py init off reinforcement


#每次使用image功能都会覆盖上一次的过程
#所以加了额外功能，调用生成GIF的程序（同时清空output文件夹）
#如果得到好的结果建议运行该函数用来展示
save:
	python3 saveImage.py output/*.png
	rm output/*.png