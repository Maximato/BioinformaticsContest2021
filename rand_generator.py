import random

with open("output/output_rg.txt", "w") as f:
    for _ in range(100000):
        f.write(str(random.randint(1, 200000)))
        f.write("\n")
