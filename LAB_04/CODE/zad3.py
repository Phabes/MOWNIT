import math
from random import randint, random
from matplotlib import pyplot as plt


def getData(file_name, separator):
  board = []
  f = open(file_name, "r")
  for line in f:
    row = line.strip().split(separator)
    for i in range(len(row)):
      if row[i] != "x":
        row[i] = int(row[i])
    board.append(row)
  f.close()
  return board


def fill_empty_fields_3x3(board):
  n = len(board)
  for i in range(n // 3):
    for j in range(n // 3):
      for k in range(1, n + 1):
        includes, y, x = includes_3x3(board, i, j, k)
        if not includes:
          board[y][x] = k


def includes_3x3(board, i, j, number):
  n = len(board)
  emptyY, emptyX = None, None
  found = False
  test_to_pass = random()
  for k in range(n):
    y = i * 3 + k // 3
    x = j * 3 + k % 3
    if board[y][x] == number:
      return True, emptyY, emptyX
    elif board[y][x] == "x":
      if found:
        test = random()
        if test > test_to_pass:
          emptyY, emptyX = y, x
      else:
        emptyY, emptyX = y, x
        found = True
  return False, emptyY, emptyX


def count_repeats(board):
  repeated = 0
  repeated += repeats_in_rows(board)
  repeated += repeats_in_columns(board)
  # repeated += repeats_in_3x3(board)  # always 0 here because 3x3 board is filled with no repeats and numbers arent swapped between 3x3 boards
  return repeated


def repeats_in_rows(board):
  n = len(board)
  repeated = 0
  count_tab = [0 for _ in range(n)]
  for line in board:
    for i in range(n):
      count_tab[i] = 0
    for element in line:
      if element != "x":
        count_tab[element - 1] += 1
    for element in count_tab:
      if element > 1:
        repeated += element - 1
  return repeated


def repeats_in_columns(board):
  n = len(board)
  repeated = 0
  count_tab = [0 for _ in range(n)]
  for i in range(n):
    for j in range(n):
      count_tab[j] = 0
    for j in range(n):
      if board[j][i] != "x":
        count_tab[board[j][i] - 1] += 1
    for element in count_tab:
      if element > 1:
        repeated += element - 1
  return repeated


def repeats_in_3x3(board):
  n = len(board)
  repeated = 0
  count_tab = [0 for _ in range(n)]
  for i in range(n // 3):
    for j in range(n // 3):
      for k in range(n):
        count_tab[k] = 0
      for k in range(n):
        y = i * 3 + k // 3
        x = j * 3 + k % 3
        if board[y][x] != "x":
          count_tab[board[y][x] - 1] += 1
      for element in count_tab:
        if element > 1:
          repeated += element - 1
  return repeated


def count_possible_fields(original_board, i, j):
  n = len(original_board)
  count = 0
  for k in range(n):
    y = i * 3 + k // 3
    x = j * 3 + k % 3
    if original_board[y][x] == "x":
      count += 1
  return count


def choose_random_fields(original_board, i, j, possible_fields):
  n = len(original_board)
  first = randint(0, possible_fields - 1)
  second = randint(0, possible_fields - 1)
  while first == second:
    second = randint(0, possible_fields - 1)
  count = 0
  if first > second:
    first, second = second, first
  p1Y, p1X = None, None
  p2Y, p2X = None, None
  for k in range(n):
    y = i * 3 + k // 3
    x = j * 3 + k % 3
    if original_board[y][x] == "x":
      if count == first:
        p1Y, p1X = y, x
      elif count == second:
        p2Y, p2X = y, x
      count += 1
  return (p1Y, p1X), (p2Y, p2X)


def solution(original_board, board, empty_fields, temp_start, temp_end, temp_iter, temp_rate):
  n = len(board)
  best = count_repeats(board)
  iterations = 0
  x_data = []
  y_data = []
  solved = False
  total = 0
  while temp_start > temp_end:
    for i in range(temp_iter):
      total+=1
      y = randint(0, n // 3 - 1)
      x = randint(0, n // 3 - 1)
      possible_fields = empty_fields[y][x]
      if possible_fields >= 2:
        p1, p2 = choose_random_fields(original_board, y, x, possible_fields)
        board[p1[0]][p1[1]], board[p2[0]][p2[1]] = board[p2[0]][p2[1]], board[p1[0]][p1[1]]
        possible = count_repeats(board)
        if possible < best:
          best = possible
          if best == 0:
            solved = True
            break
        else:
          prob = math.e ** ((best - possible) / temp_start)
          check_number = random()
          if check_number < prob:
            best = possible
          else:
            board[p1[0]][p1[1]], board[p2[0]][p2[1]] = board[p2[0]][p2[1]], board[p1[0]][p1[1]]
    x_data.append(iterations)
    y_data.append(best)
    temp_start *= temp_rate
    iterations += 1
    if solved:
      break
  print(total)
  plt.plot(x_data, y_data, "c-")
  plt.xlabel("iterations")
  plt.ylabel("f")
  # plt.show()
  return solved


if __name__ == "__main__":
  temp_start = 5230
  temp_end = 0.1
  temp_iter = 100
  temp_rate = 0.99
  file_name = "sudoku_easy.txt"
  separator = ","
  original_board = getData(file_name, separator)
  empty_fields = [[count_possible_fields(original_board, i, j) for j in range(3)] for i in range(3)]
  suma = 0
  for row in empty_fields:
    for element in row:
      suma+=element
  print(suma)
  n = len(original_board)
  board = [[original_board[i][j] for j in range(n)] for i in range(n)]
  fill_empty_fields_3x3(board)
  for line in original_board:
    print(line)
  print("FILLED")
  for line in board:
    print(line)
  found_solution = solution(original_board, board, empty_fields, temp_start, temp_end, temp_iter, temp_rate)
  print("SOLUTION")
  for line in board:
    print(line)
  print("SOLVED:", found_solution)