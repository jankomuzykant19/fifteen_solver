import time

solved = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]

empty_field = {}


# Klasa węzeł
class node:
    def __init__(self, current_board, parent, last_move, way, order):
        self.board = current_board  # Do zmiennej tablca przypisujemy obecny wygląd tablicy
        self.children = {}
        self.heu_que = {}
        if parent != 'Root':  # Jeżeli rodzic  nie jest "korzeniem"
            self.parent = parent
        self.last = last_move  # Ostatni ruch
        self.way = way.copy()  # do ścieżki ruchu przypisujemy jej kopię
        self.way.append(last_move)  # i do tej kopii dodajemy ostatni wykonany ruch
        self.to_visit = order.copy()  # to_visit to są miejsca do odwiedzenia, przypisujemy do nich kopię tego orderu który podajemy w wywołaniu

    # Tworzenie dziecka danego węzła
    def create_child(self, board_after_move, move, order):
        child = node(board_after_move, self, move, self.way, order)
        self.children[move] = child


    def make_move(self, move, order):
        y = empty_field['row']
        x = empty_field['column']
        if move == 'L':
            array = []
            for row in self.board:
                array.append(row.copy())
            array[y][x - 1], array[y][x] = array[y][x], array[y][x - 1]
            empty_field['column'] -= 1
            self.create_child(array, move, order)
        elif move == 'R':
            array = []
            for row in self.board:
                array.append(row.copy())
            array[y][x], array[y][x + 1] = array[y][x + 1], array[y][x]
            empty_field['column'] += 1
            self.create_child(array, move, order)
        elif move == 'U':
            array = []
            for row in self.board:
                array.append(row.copy())
            array[y - 1][x], array[y][x] = array[y][x], array[y - 1][x]
            empty_field['row'] -= 1
            self.create_child(array, move, order)
        elif move == 'D':
            array = []
            for row in self.board:
                array.append(row.copy())
            array[y][x], array[y + 1][x] = array[y + 1][x], array[y][x]
            empty_field['row'] += 1
            self.create_child(array, move, order)


# Zmiana pozycji pustego miejsca, w zależności od ruchu operujemy na odpowiednich współrzędnych pustego pola
def change_0_pos(last_move):
    if last_move == 'U':
        empty_field['row'] += 1
    if last_move == 'D':
        empty_field['row'] -= 1
    if last_move == 'L':
        empty_field['column'] += 1
    if last_move == 'R':
        empty_field['column'] -= 1


# Usuwamy ścieżki w które nie da się iść sprawdzając w którą stronę nie możemy przesunąć pustego miejsca
def remove_possible_ways(current_node, flag=False):
    is_l = False
    is_r = False
    is_u = False
    is_d = False
    # jest len(solved[0]) bo kolumny są jakby w jednmy okienku i dlatego sprawdzamy długość tego pierwszego wiersza
    # a len(solved) jest po to, że jest to liczba wierszy po prostu
    if empty_field['column'] == len(solved[0]) - 1 and empty_field['row'] == len(solved) - 1:
        current_node.to_visit.remove('R')
        current_node.to_visit.remove('D')
        is_r = True
        is_d = True
    elif empty_field['column'] == len(solved[0]) - 1 and empty_field['row'] == 0:
        current_node.to_visit.remove('R')
        current_node.to_visit.remove('U')
        is_r = True
        is_u = True
    elif empty_field['column'] == 0 and empty_field['row'] == 0:
        current_node.to_visit.remove('L')
        current_node.to_visit.remove('U')
        is_l = True
        is_u = True
    elif empty_field['column'] == 0 and empty_field['row'] == len(solved) - 1:
        current_node.to_visit.remove('L')
        current_node.to_visit.remove('D')
        is_l = True
        is_d = True
    elif empty_field['column'] == 0:
        current_node.to_visit.remove('L')
        is_l = True
    elif empty_field['column'] == len(solved[0]) - 1:
        current_node.to_visit.remove('R')
        is_r = True
    elif empty_field['row'] == 0:
        current_node.to_visit.remove('U')
        is_u = True
    elif empty_field['row'] == len(solved) - 1:
        current_node.to_visit.remove('D')
        is_d = True
    if not flag:
        if current_node.last == 'R' and not is_l:
            current_node.to_visit.remove('L')
        elif current_node.last == 'L' and not is_r:
            current_node.to_visit.remove('R')
        elif current_node.last == 'U' and not is_d:
            current_node.to_visit.remove('D')
        elif current_node.last == 'D' and not is_u:
            current_node.to_visit.remove('U')


# Funkcja sprawdzająca czy już rozwiązaliśmy
def is_solved(test_board, solved):
    if test_board == solved:
        return True


# Funkcja szukająca pustego pola
def find_empty_field(test_board):
    for j in range(len(test_board)):
        for i in range(len(test_board[j])):
            if test_board[j][i] == '0':
                empty_field['row'] = j
                empty_field['column'] = i
    return empty_field


# Funkcja przygotowująca rozwiązanie
def prepare_solution(data, solution_file, statistic_file, s_time):
    way, processed_nodes, visited_nodes, depth_level = data
    if way != -1:  # Jeżeli znajdzie rozwiązanie
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
        file.write(str(solution).replace(" ", "").replace("'", "").replace("[", "").replace("]", "").replace(",", ""))
    file.close()
    file = open(statistic_file, 'w+')
    file.write(str(solution_length) + '\n')
    file.write(str(visited_nodes) + '\n')
    file.write(str(processed_nodes) + '\n')
    file.write(str(depth_level) + '\n')
    file.write(str(round((time.time() - s_time) * 1000, 3)))
    file.close()
