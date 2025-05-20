import random

num = random.randint(1,1000)
bin="{0:b}".format(num)
while True:
    inp=int(input(f"Enter the decimal equivelant of the binary number {bin}\n"))
    if inp == num:
        print("correct!")
        break
    elif inp > num:
        print("Too high!")
    else:
        print("Too low!")
print("gg")