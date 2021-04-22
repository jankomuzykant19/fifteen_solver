import random
import time

import node as n


def dfs(start_time, start_board, order, solved, depth):
    amount_of_processed_nodes = 1
    amount_of_visited_nodes = 1
    current_node = n.node(start_board, 'Root', None, [], order)
    root_flag = True
    parent_flag = False
    max_depth = False
    depth_level = 0
    n.remove_ways_to_out_of_board(current_node, root_flag)
    while True:
        if n.is_solved(current_node.board, solved):
            if max_depth:
                depth_level = depth
            else:
                depth_level = len(current_node.way) - 1
            return current_node.way, amount_of_processed_nodes, amount_of_visited_nodes, depth_level
        elif len(current_node.way) == depth:
            current_node = current_node.parent
            n.find_and_set_empty_field(current_node.board)
            parent_flag = True
            max_depth = True
        elif len(current_node.to_visit) != 0:
            if not root_flag and not parent_flag:
                n.remove_ways_to_out_of_board(current_node)
            if len(current_node.to_visit) != 0:
                move = current_node.to_visit[0]
                current_node.make_move(move, order)
                current_node.to_visit.remove(move)
                current_node = current_node.children[move]
                n.find_and_set_empty_field(current_node.board)
                root_flag = False
                parent_flag = False
                amount_of_visited_nodes += 1
                amount_of_processed_nodes += 1
            else:
                if current_node.last is None or time.time() - start_time > depth:
                    return -1, amount_of_processed_nodes, amount_of_visited_nodes, depth_level
                else:
                    current_node = current_node.parent
                    find_and_set_empty_field(current_node.board)
                    parent_flag = True
        else:
            if current_node.last is None or time.time() - start_time > depth:
                return -1, amount_of_processed_nodes, amount_of_visited_nodes, depth_level
            else:
                current_node = current_node.parent
                n.find_and_set_empty_field(current_node.board)
                parent_flag = True


def bfs(start_time, start_board, order, solved, depth):
    amount_of_processed_nodes = 1
    amount_of_visited_nodes = 1
    current_node = n.node(start_board, 'Root', None, [], order)
    n.remove_ways_to_out_of_board(current_node, True)
    queue = []
    counter = 0
    while True:
        counter += 1
        if time.time() - start_time > depth:
            return -1, amount_of_processed_nodes, amount_of_visited_nodes, len(current_node.way) - 1
        if n.is_solved(current_node.board, solved):
            return current_node.way, amount_of_processed_nodes, amount_of_visited_nodes, len(current_node.way) - 1
        else:
            if not current_node.last is None:
                n.remove_ways_to_out_of_board(current_node, False)
            for move in current_node.to_visit:
                amount_of_processed_nodes += 1
                current_node.make_move(move, order)
                current_node = current_node.children[move]
                queue.append(current_node)
                last_move = current_node.way[-1]
                n.change_position_of_blank_field(last_move)
                current_node = current_node.parent
            try:
                if current_node.last is not None:
                    queue.remove(current_node)
            except ValueError:
                pass
            current_node = queue[0]
            amount_of_visited_nodes += 1
            n.find_and_set_empty_field(current_node.board)


def astr(heuristic, start_time, start_board, order, solved, depth):
    amount_of_visited_nodes = 1
    amount_of_processed_nodes = 1

    def get_index_of_value(board, value):
        for index_row, row in enumerate(board):
            for index_col, elem in enumerate(row):
                if elem == value:
                    return index_row, index_col

    if heuristic == 'manh':
        def calculate_error(current_board, solved):
            manh_error = 0
            for index_row, row in enumerate(current_board):
                for index_col, elem in enumerate(row):
                    target_row, target_col = get_index_of_value(solved, elem)
                    manh_error += abs(index_row - target_row) + abs(index_col - target_col)
                    print(manh_error)
            return manh_error
    else:
        def calculate_error(current_board, solved):
            hamm_error = 0
            for index_row, row in enumerate(current_board):
                for index_col, elem in enumerate(row):
                    target_row, target_col = get_index_of_value(solved, elem)
                    if abs(index_row - target_row) + abs(index_col - target_col) != 0:
                        hamm_error += 1
            return hamm_error
    current_node = n.node(start_board, 'Root', None, [], order)
    n.remove_ways_to_out_of_board(current_node, True)
    while True:
        try:
            if time.time() - start_time > depth:
                return -1, amount_of_processed_nodes, amount_of_visited_nodes, len(current_node.way) - 1
            if n.is_solved(current_node.board, solved):
                return current_node.way, amount_of_processed_nodes, amount_of_visited_nodes, len(current_node.way) - 1
            else:
                for move in current_node.to_visit:
                    amount_of_processed_nodes += 1
                    current_node.make_move(move, order)
                    current_node = current_node.children[move]
                    error = calculate_error(current_node.board, solved)
                    current_node = current_node.parent
                    n.find_and_set_empty_field(current_node.board)
                    current_node.errors[move] = error
                min_value = min(current_node.errors.values())
                tmp = []
                for key in current_node.errors:
                    if current_node.errors[key] == min_value:
                        tmp.append(key)
                nr = random.randint(0, len(tmp) - 1)
                next_move = tmp[nr]
                current_node.make_move(next_move, order)
                current_node = current_node.children[next_move]
                amount_of_visited_nodes += 1
                try:
                    n.remove_ways_to_out_of_board(current_node, False)
                except ValueError:
                    pass
        except MemoryError:
            return -1, amount_of_processed_nodes, amount_of_visited_nodes, len(current_node.way) - 1
