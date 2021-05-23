#saveImage.py

#将output文件夹下的图片生成GIF

import imageio
import sys

def compose_gif(str):
    gif_images = []
    for path in str:
        gif_images.append(imageio.imread(path))
    imageio.mimsave("output.gif", gif_images, fps=1)

str = []
for i in range(1,len(sys.argv)):
    str.append(sys.argv[i])
compose_gif(str)