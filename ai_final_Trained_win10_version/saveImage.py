#saveImage.py

#将output文件夹下的图片生成GIF

import imageio
import sys

def compose_gif(str, name):
    gif_images = []
    for path in str:
        gif_images.append(imageio.imread(path))
    imageio.mimsave(name, gif_images, fps=0.5)

print("\n正在生成gif...")
str = []
if len(sys.argv) == 3:
    print("[Error!]output文件夹没有任何图片！")
else:
    for i in range(2,len(sys.argv)):
        str.append(sys.argv[i])
    name = "output/"+ sys.argv[1]
    compose_gif(str, name)
    print("生成过程记录成功！")
