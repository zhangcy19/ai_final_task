import sys
import os

with open("assist_data/score.txt", "r") as f:
    score = f.read()

for i in range(1, len(sys.argv)):
    with open(sys.argv[i], "r") as f:
        temp = f.read()

    if temp > score:
        with open("assist_data/score.txt", "w") as f:
            f.write(temp)
    os.system("rm \"%s\""%sys.argv[i])

