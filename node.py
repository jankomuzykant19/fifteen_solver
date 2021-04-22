import time

solved = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]

EMPTY_FIELD = {}


class node:
    def __init__(self, current_board, parent, last_move, way, order):
        self.board = current_board
        self.children = {}
        self.errors = {}
        if parent != 'Root':
            self.parent = parent
        self.last = last_move
        self.way = way.copy()
        self.way.append(last_move)
        self.to_visit = order.copy()

    def create_child(self, board_after_move, move, order):
        child = node(board_after_move, self, move, self.way, order)
        self.children[move] = child

    def make_move(self, move, order):
        y = EMPTY_FIELD['row']
        x = EMPTY_FIELD['column']
        array = []
        if move == 'L':
            for row in self.board:
                array.append(row.copy())
            array[y][x - 1], array[y][x] = array[y][x], array[y][x - 1]
            EMPTY_FIELD['column'] -= 1
            self.create_child(array, move, order)
        elif move == 'R':
            for row in self.board:
                array.append(row.copy())
            array[y][x], array[y][x + 1] = array[y][x + 1], array[y][x]
            EMPTY_FIELD['column'] += 1
            self.create_child(array, move, order)
        elif move == 'U':
            for row in self.board:
                array.append(row.copy())
            array[y - 1][x], array[y][x] = array[y][x], array[y - 1][x]
            EMPTY_FIELD['row'] -= 1
            self.create_child(array, move, order)
        elif move == 'D':
            for row in self.board:
                array.append(row.copy())
            array[y][x], array[y + 1][x] = array[y + 1][x], array[y][x]
            EMPTY_FIELD['row'] += 1
            self.create_child(array, move, order)


def change_position_of_blank_field(last_move):
    if last_move == 'U':
        EMPTY_FIELD['row'] += 1
    if last_move == 'D':
        EMPTY_FIELD['row'] -= 1
    if last_move == 'L':
        EMPTY_FIELD['column'] += 1
    if last_move == 'R':
        EMPTY_FIELD['column'] -= 1


def remove_ways_to_out_of_board(current_node, flag=False):
    is_removed_l = False
    is_removed_r = False
    is_removed_u = False
    is_removed_d = False
    if EMPTY_FIELD['column'] == len(solved[0]) - 1 and EMPTY_FIELD['row'] == len(solved) - 1:
        current_node.to_visit.remove('R')
        current_node.to_visit.remove('D')
        is_removed_r = True
        is_removed_d = True
    elif EMPTY_FIELD['column'] == len(solved[0]) - 1 and EMPTY_FIELD['row'] == 0:
        current_node.to_visit.remove('R')
        current_node.to_visit.remove('U')
        is_removed_r = True
        is_removed_u = True
    elif EMPTY_FIELD['column'] == 0 and EMPTY_FIELD['row'] == 0:
        current_node.to_visit.remove('L')
        current_node.to_visit.remove('U')
        is_removed_l = True
        is_removed_u = True
    elif EMPTY_FIELD['column'] == 0 and EMPTY_FIELD['row'] == len(solved) - 1:
        current_node.to_visit.remove('L')
        current_node.to_visit.remove('D')
        is_removed_l = True
        is_removed_d = True
    elif EMPTY_FIELD['column'] == 0:
        current_node.to_visit.remove('L')
        is_removed_l = True
    elif EMPTY_FIELD['column'] == len(solved[0]) - 1:
        current_node.to_visit.remove('R')
        is_removed_r = True
    elif EMPTY_FIELD['row'] == 0:
        current_node.to_visit.remove('U')
        is_removed_u = True
    elif EMPTY_FIELD['row'] == len(solved) - 1:
        current_node.to_visit.remove('D')
        is_removed_d = True
    if not flag:
        if current_node.last == 'R' and not is_removed_l:
            current_node.to_visit.remove('L')
        elif current_node.last == 'L' and not is_removed_r:
            current_node.to_visit.remove('R')
        elif current_node.last == 'U' and not is_removed_d:
            current_node.to_visit.remove('D')
        elif current_node.last == 'D' and not is_removed_u:
            current_node.to_visit.remove('U')


def is_solved(test_board, solved):
    if test_board == solved:
        return True


def find_and_set_empty_field(test_board):
    for j in range(len(test_board)):
        for i in range(len(test_board[j])):
            if test_board[j][i] == '0':
                EMPTY_FIELD['row'] = j
                EMPTY_FIELD['column'] = i


def prepare_solution(data, solution_file, statistic_file, s_time):
    way, processed_nodes, visited_nodes, depth_level = data
    if way != -1:
        way.remove(way[0])
        solution_length = len(way)
        solution = way
    else:
        solution_length = -1
        solution = []
    file = open(solution_file, 'w+')
    file.write(str(solution_length))
    if way != -1:
        file.write('\n')
        file.write(str(solution))
    file.close()
    file = open(statistic_file, 'w+')
    file.write(str(solution_length))
    file.write('\n')
    file.write(str(visited_nodes))
    file.write('\n')
    file.write(str(processed_nodes))
    file.write('\n')
    file.write(str(depth_level))
    file.write('\n')
    file.write(str(round((time.time() - s_time) * 1000, 3)))
    file.close()
