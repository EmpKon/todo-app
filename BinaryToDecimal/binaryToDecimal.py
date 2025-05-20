import random

num = random.randint(1,1000)
bin="{0:b}".format(num)
while True:
    inp=input(f"Enter the decimal equivelant of the binary number {bin}\n")
    if inp == bin:
        print("correct!")
        break
    elif inp > bin:
        print("Too high!")
    else:
        print("Too low!")
print("gg")