import argparse
import time

import algorithms as a
import node as n

solved = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'],
          ['13', '14', '15', '0']]  # Rozwiązana plansza
start = []  # Pusta startowa plansza
empty_field = {}  # Nasze "0" czyli puste pole {} - słownik
depth = 20  # Ustawiamy głębokość na 20

args = argparse.ArgumentParser(
    description="Insert following argumets: algorithm, order, input file, output file, stats file")  # Dodajemy odpowiednie argumenty z wywołania
args.add_argument("algorithm")
args.add_argument("order")
args.add_argument("input_file")
args.add_argument("output_file")
args.add_argument("stats_file")
sizee = []
arguments = args.parse_args()  # Tworzymy zmienną do której przypisujemy wszystkie argumenty
print(arguments)

with open(arguments.input_file) as file:  # Bierzemy argument input_file i wczytujemy go
    size_flag = True  # Pierwsza linia to rozmiar planszy np: "4 4" nie wczytujemy tego
    for line in file:
        if size_flag:
            size_flag = False
            sizee.append(line)
        else:
            start.append(line.split())
    solved_flexi = []
# for i in range(int(str(sizee)[2])*int(str(sizee)[4])-1):
#    solved_flexi.append()
# mm = int(str(sizee)[2])
# nn = int(str(sizee)[4])
#
# tabi = [[0] * mm for i in range(nn)]
#
# count = 0
# for row in range(mm):
#     for col in range(nn):
#         tabi[col][row] = col + 1 + count * nn
#     count += 1
#
# tabi[nn - 1][mm - 1] = 0

#
# print(solved_flexi)

order = []  # Tworzymy listę tych literek z argumentu order
for elem in arguments.order:  # Robimy to po to aby litery były osobno w liście
    order.append(elem)

n.find_empty_field(start)  # Wywołujemy funkcję która szuka "0" w początkowej tablicy
start_time = time.time()  # Ustalamy czas początkowy
# Ustalamy jaki argument został wybrany
if arguments.algorithm == 'dfs':
    n.prepare_solution(a.dfs(start_time, start, order, solved, depth), arguments.output_file, arguments.stats_file,
                       start_time)
elif arguments.algorithm == 'bfs':
    n.prepare_solution(a.bfs(start_time, start, order, solved, depth), arguments.output_file, arguments.stats_file,
                       start_time)
else:
    if arguments.order == 'manh':
        # print("jestem tu manh")
        order = ['L', 'U', 'D', 'R']
        n.prepare_solution(a.astr(arguments.order, start_time, start, order, solved, depth), arguments.output_file,
                           arguments.stats_file, start_time)
    else:
        # print("jestem tu hamm")
        order = ['U', 'L', 'R', 'D']
        n.prepare_solution(a.astr(arguments.order, start_time, start, order, solved, depth), arguments.output_file,
                           arguments.stats_file, start_time)
