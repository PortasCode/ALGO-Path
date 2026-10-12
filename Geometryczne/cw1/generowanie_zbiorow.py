import random
from math import sin, cos, radians


# Generowanie zbioru A
def generate_setA():
    with open("setA_points.csv", "w") as f:
        for _ in range(10**5):
            x = random.uniform(-1000, 1000)
            y = random.uniform(-1000, 1000)
            f.write(f"{x},{y}\n")


# Generowanie zbioru B
def generate_setB():
    with open("setB_points.csv", "w") as f:
        for _ in range(10**5):
            x = random.uniform(-(10**14), 10**14)
            y = random.uniform(-(10**14), 10**14)
            f.write(f"{x},{y}\n")


# Generowanie zbioru C
def generate_setC():
    with open("setC_points.csv", "w") as f:
        R = 100
        for _ in range(1000):
            stopnie = random.uniform(0, 360)
            rad = radians(stopnie)

            x = R * cos(rad)
            y = R * sin(rad)

            f.write(f"{x},{y}\n")


# Generowanie zbioru D
def generate_setD():
    with open("setD_points.csv", "w") as f:
        A = 0.05
        B = 0.05
        for _ in range(1000):
            x = random.uniform(-1000, 1000)
            y = A * x + B

            f.write(f"{x},{y}\n")


if __name__ == "__main__":
    generate_setA()
    generate_setB()
    generate_setC()
    generate_setD()
