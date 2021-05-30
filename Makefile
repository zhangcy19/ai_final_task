#usage: main.py [sample/heuristic/reinforcement] [-off]

#[sample/heuristic/reinforcement]：必选项，分别对应不同算法
#[-off] 可选项，使用后不再调用绘制函数，没有图片输出

sam:
	python3 main.py sample
samf:
	python3 main.py sample off
heu:
	python3 main.py heuristic
rein:
	python3 main.py reinforcement