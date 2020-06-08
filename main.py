from __future__ import print_function
import copy
import math
import random
import sys
from time import perf_counter

x = [0]
best = [0]
start_pos = []
my_map = []
c = 5
choices = [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2], [0, 1, 2, 3]]


def nums(n):
    num = []
    for i in range(n):
        num.append(i)

    return num


def my_split(line):
    return list(map(int, [digit for digit in line]))


def whole_rand(n):
    return round(random.randint(0, n))


def get_input():
    my_input = []
    line = input().split()
    my_input.append(int(line[0]))
    my_input.append(int(line[1]))
    my_input.append(int(line[2]))

    for i in range(my_input[1]):
        my_input.append(my_split(input()))

    my_input.append([char for char in input()])

    return my_input


def gen_seq(m, n):
    my_seq = []
    for i in range(m * n):
        my_seq.append(whole_rand(3))

    return my_seq


def wheres_waldo():
    global my_map
    waldo = [0, 0]

    for i in range(len(my_map)):
        for j in range(len(my_map[1])):
            if my_map[i][j] == 5:
                waldo = [i, j]

    return waldo


def take_step(path, walked, curr_pos, idx):
    # print(path, idx)
    if path[idx] == 0:  # RIGHT
        try:
            if my_map[curr_pos[0]][curr_pos[1] + 1] == 0:
                curr_pos[1] += 1
                walked.append(path[idx])

            elif my_map[curr_pos[0]][curr_pos[1] + 1] == 1:
                pass

            elif my_map[curr_pos[0]][curr_pos[1] + 1] == 2:
                pass

            elif my_map[curr_pos[0]][curr_pos[1] + 1] == 3:
                curr_pos[1] += 1
                walked.append(path[idx])

        except IndexError:
            pass

    elif path[idx] == 1:  # LEFT
        try:
            if my_map[curr_pos[0]][curr_pos[1] - 1] == 0:
                curr_pos[1] -= 1
                walked.append(path[idx])

            elif my_map[curr_pos[0]][curr_pos[1] - 1] == 1:
                pass

            elif my_map[curr_pos[0]][curr_pos[1] - 1] == 2:
                pass

            elif my_map[curr_pos[0]][curr_pos[1] - 1] == 3:
                curr_pos[1] -= 1
                walked.append(path[idx])

        except IndexError:
            pass

    elif path[idx] == 2:  # DOWN
        try:
            if my_map[curr_pos[0] + 1][curr_pos[1]] == 0:
                curr_pos[0] += 1
                walked.append(path[idx])

            elif my_map[curr_pos[0] + 1][curr_pos[1]] == 1:
                pass

            elif my_map[curr_pos[0] + 1][curr_pos[1]] == 2:
                curr_pos[0] += 1
                walked.append(path[idx])

            elif my_map[curr_pos[0] + 1][curr_pos[1]] == 3:
                pass

        except IndexError:
            pass

    elif path[idx] == 3:  # UP
        try:
            if my_map[curr_pos[0] - 1][curr_pos[1]] != 1:
                curr_pos[0] -= 1
                walked.append(path[idx])

            elif my_map[curr_pos[0] - 1][curr_pos[1]] == 1:
                pass

            elif my_map[curr_pos[0] - 1][curr_pos[1]] == 2:
                curr_pos[0] += 1
                walked.append(path[idx])

            elif my_map[curr_pos[0] - 1][curr_pos[1]] == 3:
                pass

        except IndexError:
            pass


def walk(temp):
    global x
    global best
    global my_map
    global start_pos
    global c

    for i in range(400):
        curr_pos = start_pos[::]
        walked = []
        x = perturb()

        for idx in range(len(x)):
            take_step(x, walked, curr_pos, idx)
            if my_map[curr_pos[0]][curr_pos[1]] == 8:
                # print("FINISHED")

                if len(x) > len(walked):
                    eprint("found shorter:", len(walked))

                x = walked[::]
                if len(x) < len(best):
                    best = x[::]

                return

    n_idx = len(x)
    walked = x[::]
    while True:
        walked.append(random.randint(0, 3))
        take_step(walked, walked, curr_pos, n_idx)
        n_idx += 1

        if my_map[curr_pos[0]][curr_pos[1]] == 8:
            # print("FINISHED")

            try:
                p = 1.0 / (1 + math.e ** ((c * (len(walked) - len(x))) / temp))
            except OverflowError:
                p = 0

            # print(p)
            if random.random() <= p:
                eprint("len x:", len(x), "len walked:", len(walked), "temp:", temp, "prob:", p)
                x = walked[::]

            return


def search_lab():
    global my_map
    global x
    global best
    global start_pos

    time = my_map.pop(0)
    m = my_map.pop(0)
    n = my_map.pop(0)
    x = from_char(my_map.pop(m))
    best = x[::]
    start_pos = wheres_waldo()
    temp = time**2 * 3
    iters = 0

    eprint('1st path: ', x)
    eprint(len(x))

    t_start = perf_counter()
    while time > perf_counter() - t_start:
        temp = temp * 0.99

        walk(temp)

        iters += 1

    eprint("iterations:", iters)

    return best


def perturb():
    global x
    global choices
    copied = copy.deepcopy(x)
    for i in range(int(len(copied) * 0.15)):
        idx = whole_rand(len(copied) - 1)
        try:
            if copied[idx-1] == 0:
                copied[idx] = random.choice(choices[1])
            elif copied[idx - 1] == 1:
                copied[idx] = random.choice(choices[0])
            elif copied[idx - 1] == 2:
                copied[idx] = random.choice(choices[3])
            elif copied[idx - 1] == 3:
                copied[idx] = random.choice(choices[2])

        except IndexError:
            copied[idx] = random.choice(choices[4])

    return copied


def to_char(my_path):
    chars = []
    for i in range(len(my_path)):
        if my_path[i] == 0:
            chars.append("R")
        elif my_path[i] == 1:
            chars.append("L")
        elif my_path[i] == 2:
            chars.append("D")
        elif my_path[i] == 3:
            chars.append("U")

    return chars


def from_char(my_path):
    ints = []
    for i in range(len(my_path)):
        if my_path[i] == "R":
            ints.append(0)
        elif my_path[i] == "L":
            ints.append(1)
        elif my_path[i] == "D":
            ints.append(2)
        elif my_path[i] == "U":
            ints.append(3)

    return ints


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


my_map = get_input()
my_best = search_lab()
print(len(my_best))
eprint(to_char(my_best))
