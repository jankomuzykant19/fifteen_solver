import random
import time

import node as n


# DFS sprawdza po kolei każdą gałąź po gałęzi
# Wybiera węzeł, jeżeli był nieodwiedzony to oznacza go jako odwiedzonego i
# potwarza się dla sąsiadujących węzłów.
# Algorytm powtarza się dopóki wszystkie węzły nie są odwiedzone lub do momentu aż tablice będą identyczne
def dfs(start_time, start_board, order, solved, depth):
    processed_nodes = 1  # przetworzone węzły
    visited_nodes = 1  # odwiedzone węzły
    current_node = n.node(start_board, 'Root', None, [], order)  # tworzymy obecny węzeł
    root_flag = True  # flaga korzenia
    parent_flag = False  # flaga rodzinca
    max_depth = False  # flaga maksymalnej głębokości
    depth_level = 0
    n.remove_possible_ways(current_node, root_flag)
    while True:
        if n.is_solved(current_node.board, solved):  # sprawdzamy czy mamy rozwiązanie
            if max_depth:
                depth_level = depth
            else:
                depth_level = len(current_node.way) - 1
            return current_node.way, processed_nodes, visited_nodes, depth_level
        elif len(current_node.way) == depth:
            current_node = current_node.parent
            n.find_empty_field(current_node.board)
            parent_flag = True
            max_depth = True
        elif len(current_node.to_visit) != 0:
            if not root_flag and not parent_flag:
                n.remove_possible_ways(current_node)
            if len(current_node.to_visit) != 0:
                move = current_node.to_visit[0]
                current_node.make_move(move, order)
                current_node.to_visit.remove(move)
                current_node = current_node.children[move]
                n.find_empty_field(current_node.board)
                root_flag = False
                parent_flag = False
                visited_nodes += 1
                processed_nodes += 1
            else:
                if current_node.last is None or time.time() - start_time > depth:
                    return -1, processed_nodes, visited_nodes, depth_level
                else:
                    current_node = current_node.parent
                    find_empty_field(current_node.board)
                    parent_flag = True
        else:
            if current_node.last is None or time.time() - start_time > depth:
                return -1, processed_nodes, visited_nodes, depth_level
            else:
                current_node = current_node.parent
                n.find_empty_field(current_node.board)
                parent_flag = True


# BFS sprawdza po kolei każdy poziom po poziomie drzewa
def bfs(start_time, start_board, order, solved, depth):
    processed_nodes = 1
    visited_nodes = 1
    current_node = n.node(start_board, 'Root', None, [], order)
    n.remove_possible_ways(current_node, True)
    queue = []
    counter = 0
    while True:
        counter += 1
        if time.time() - start_time > depth:
            return -1, processed_nodes, visited_nodes, len(current_node.way) - 1
        if n.is_solved(current_node.board, solved):
            return current_node.way, processed_nodes, visited_nodes, len(current_node.way) - 1
        else:
            if current_node.last is not None:
                n.remove_possible_ways(current_node, False)
            for move in current_node.to_visit:
                processed_nodes += 1
                current_node.make_move(move, order)
                current_node = current_node.children[move]
                queue.append(current_node)
                last_move = current_node.way[-1]
                n.change_0_pos(last_move)
                current_node = current_node.parent
            try:
                if current_node.last is not None:
                    queue.remove(current_node)
            except ValueError:
                pass
            current_node = queue[0]
            visited_nodes += 1
            n.find_empty_field(current_node.board)


# Funkcja szukająca w którym miejscu na planszy znajduje się dana wartość
def get_index_of_value(board, value):
    for index_row, row in enumerate(board):
        for index_col, elem in enumerate(row):
            if elem == value:
                return index_row, index_col


# Funkcja która liczy heurystyki
def calculate_heu(current_board, solved, heuristic):
    if heuristic == 'manh':
        # print("manh tu byl")
        manh = 0
        for index_row, row in enumerate(current_board):
            for index_col, elem in enumerate(row):
                if elem != '0':
                    target_row, target_col = get_index_of_value(solved, elem)
                    manh += abs(index_row - target_row) + abs(index_col - target_col)
        return manh
    else:
        hamm = 0
        for index_row, row in enumerate(current_board):
            for index_col, elem in enumerate(row):
                if elem != '0':
                    target_row, target_col = get_index_of_value(solved, elem)
                    if abs(index_row - target_row) + abs(index_col - target_col) != 0:
                        hamm += 1
        return hamm


def astr(heuristic, start_time, start_board, order, solved, depth):
    visited_nodes = 1
    processed_nodes = 1
    current_node = n.node(start_board, 'Root', None, [], order)
    n.remove_possible_ways(current_node, True)
    while True:
        try:
            if time.time() - start_time > depth:
                return -1, processed_nodes, visited_nodes, len(current_node.way) - 1
            if n.is_solved(current_node.board, solved):
                return current_node.way, processed_nodes, visited_nodes, len(current_node.way) - 1
            else:
                processed_nodes += 1
                for move in current_node.to_visit:
                    current_node.make_move(move, order)
                    current_node = current_node.children[move]
                    #print(len(current_node.way))
                    error = calculate_heu(current_node.board, solved, heuristic)
                    #print(error)
                    current_node = current_node.parent
                    n.find_empty_field(current_node.board)
                    current_node.heu_que[move] = error
                min_value = min(current_node.heu_que.values())
                #print("Min:",min_value)
                #print("Que", current_node.heu_que)
                tmp = []
                for key in current_node.heu_que:
                    if current_node.heu_que[key] == min_value:
                        tmp.append(key)
                #print(tmp)
                nr = random.randint(0, len(tmp) - 1)
                print(nr)
                next_move = tmp[nr]
                current_node.make_move(next_move, order)
                current_node = current_node.children[next_move]
                visited_nodes += 1
                try:
                    n.remove_possible_ways(current_node, True)
                except ValueError:
                    pass
        except MemoryError:
            return -1, processed_nodes, visited_nodes, len(current_node.way) - 1
