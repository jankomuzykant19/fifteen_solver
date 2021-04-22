import argparse
import time

import algorithms as a
import node as n

solved = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
start = []
EMPTY_FIELD = {}
depth = 20

args = argparse.ArgumentParser(
    description="Insert following argumets: algorithm, order, input file, output file, stats file")
args.add_argument("algorithm")
args.add_argument("order")
args.add_argument("input_file")
args.add_argument("output_file")
args.add_argument("stats_file")

arguments = args.parse_args()
print(arguments)

with open(arguments.input_file) as file:
    size_flag = True
    for line in file:
        if size_flag:
            size_flag = False
            continue
        else:
            start.append(line.split())

    print(start)

order = []
for elem in arguments.order:  # robimy to po to aby litery były osobno
    order.append(elem)

n.find_and_set_empty_field(start)
start_time = time.time()
if arguments.algorithm == 'dfs':
    n.prepare_solution(a.dfs(start_time, start, order, solved, depth), arguments.output_file, arguments.stats_file,
                       start_time)
elif arguments.algorithm == 'bfs':
    n.prepare_solution(a.bfs(start_time, start, order, solved, depth), arguments.output_file, arguments.stats_file,
                       start_time)
else:
    order = ['L', 'R', 'D', 'U']
    if order == 'manh':
        n.prepare_solution(a.astr('manh', start_time, start, order, solved, depth), arguments.output_file,
                           arguments.stats_file, start_time)
    else:
        n.prepare_solution(a.astr('hamm', start_time, start, order, solved, depth), arguments.output_file,
                           arguments.stats_file, start_time)
