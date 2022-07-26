# -*- coding: utf-8 -*-
import random


def form_zero_matrix(size):
    matrix_in = dict()
    for i in range(size):
        for j in range(size):
            if j == 0:
                matrix_in[i] = {j: 0}
            else:
                matrix_in[i].update({j: 0})
    return matrix_in


def form_zero_column(i, size):
    global columns

    for j in range(size):
        columns[j][i] = 0


def form_zero_boxrow(ii, size):
    global box

    for jj in range(size):
        key = getboxnum(ii, jj)
        col = getboxcol(key, ii, jj)
        box[key][col] = 0


def box_assign(size):
    if size % 2 == 0:
        num_row = 2
        num_col = int(size / 2)
    else:
        num_row = num_col = 3

    box = dict()
    box_num = 0
    box[box_num] = []
    num_sidebox = num_row
    num_downbox = num_col

    for row in range(num_downbox):
        for col in range(num_sidebox):
            for i in range(0 + (row * num_row), num_row + (row * num_row)):
                for j in range(0 + (col * num_col), num_col + (col * num_col)):
                    box[box_num].append((i, j))
            if box_num < (size - 1):
                box_num += 1
                box[box_num] = []
    return box


def check_exist(number, ii, jj):
    global box, columns, sizeofsudoku, temp_list

    key = getboxnum(ii, jj)
    temporary = temp_list.copy()

    while True:
        if number in columns[jj].values() or number in box[key].values():
            if len(temporary) > 0:
                number = random.choice(temporary)
                temporary.remove(number)
            else:
                return 0
        else:
            return number


def getboxnum(ii, jj):
    global box_index

    for key in box_index.keys():
        if (ii, jj) in box_index[key]:
            return key


def getboxcol(key, ii, jj):
    global box_index, sizeofsudoku

    for i in range(sizeofsudoku):
        if (ii, jj) == box_index[key][i]:
            return i


def check_error():
    while True:
        try:
            sizeofsudoku = int(input("Please enter the size of sudoko (4,6 or 9) :"))
            if sizeofsudoku not in (4, 6, 9):
                raise Exception("You can enter 4, 6 or 9 only. Please try again")
        except ValueError:
            print("Please enter an integer. Try again")
        except Exception as error:
            print(error)
        else:
            return sizeofsudoku


def getrandomindx(size):
    global box_index

    while True:
        difficulty = input("Please enter difficulty level. 1- Medium   2-Hard")
        if difficulty == "1":
            Level = list(range(int((size ** 2 / 2) - size / 2), int(size ** 2 / 2)))
            break
        elif difficulty == "2":
            Level = list(range(int(size ** 2 / 2), int((size ** 2 / 2) + size / 2)))
            break
        else:
            print("Wrong choice!!! Please try again")

    num_deleted = random.choice(Level)
    central = int(size / 2)
    indexes = {(central, central)}
    aggregate = []
    for i in range(size):
        aggregate += box_index[i]

    while len(indexes) < num_deleted:
        choice = random.choice(aggregate)
        indexes.add(choice)

    return indexes


sizeofsudoku = check_error()

matrix = form_zero_matrix(sizeofsudoku)
columns = form_zero_matrix(sizeofsudoku)
box = form_zero_matrix(sizeofsudoku)
box_index = box_assign(sizeofsudoku)
num_list = list(range(1, (sizeofsudoku + 1)))
count = 0
start = 0
while True:
    for i in range(start, sizeofsudoku):
        temp_list = num_list.copy()
        for j in range(sizeofsudoku):
            temp = random.choice(temp_list)
            if i == 0:
                matrix[i][j] = temp
                columns[j][i] = temp
                boxkey = getboxnum(i, j)
                boxcol = getboxcol(boxkey, i, j)
                box[boxkey][boxcol] = temp
            else:
                temp = check_exist(temp, i, j)
                if temp == 0:
                    break
                matrix[i][j] = temp
                columns[j][i] = temp
                boxkey = getboxnum(i, j)
                boxcol = getboxcol(boxkey, i, j)
                box[boxkey][boxcol] = temp
            temp_list.remove(temp)
        if temp == 0:
            start = i
            form_zero_column(i, sizeofsudoku)
            form_zero_boxrow(i, sizeofsudoku)
            count += 1
            break
    if i == (sizeofsudoku - 1):
        break
    elif count > 100:
        columns = form_zero_matrix(sizeofsudoku)
        box = form_zero_matrix(sizeofsudoku)
        count = 0
        start = 0

if sizeofsudoku == 4:
    row = 2
    col = 2
elif sizeofsudoku == 6:
    row = 2
    col = 3
else:
    row = col = 3

print()
print("{:^60}".format('The Solution of Sudoku'))
print("-" * (sizeofsudoku * 3), "-" * row, "-", sep='')
for i in range(sizeofsudoku):
    print("| ", end='')
    for j in range(sizeofsudoku):
        if (j + 1) % col == 0:
            print(matrix[i][j], " | ", sep='', end='')
        else:
            print(matrix[i][j], " ", end='')
    print()
    if (i + 1) % row == 0:
        print("-" * (sizeofsudoku * 3), "-" * row, "-", sep='')

indexlist = getrandomindx(sizeofsudoku)

print()
print("{:^60}".format('The Puzzle of Sudoku'))
print("-" * (sizeofsudoku * 3), "-" * row, "-", sep='')
for i in range(sizeofsudoku):
    print("| ", end='')
    for j in range(sizeofsudoku):
        if (j + 1) % col == 0:
            if (i, j) in indexlist:
                print(" ", " | ", sep='', end='')
            else:
                print(matrix[i][j], " | ", sep='', end='')
        else:
            if (i, j) in indexlist:
                print(" ", " ", end='')
            else:
                print(matrix[i][j], " ", end='')
    print()
    if (i + 1) % row == 0:
        print("-" * (sizeofsudoku * 3), "-" * row, "-", sep='')

input("Please press enter to exit")