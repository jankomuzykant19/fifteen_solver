# fifteen_solver

This app requires following argumets: algorithm, order, input file, output file, stats file.
Boards which can be solved are included in 413ukladow.zip 
App solves "fifteen game" using DFS, BFS and ASTR algorithms.
For DFS and BFS second argument has to be one of orders: RDUL, RDLU, DRUL, DRLU, LUDR, LURD, ULDR, ULRD
For ASTR algorithm secound argument has to be of two metrics: hamm or manh

input file is file with unsolved board form 413ukladow.zip
output file is file with two lines: first line is amount of moves of found solution, second line is sequence of n letters telling us where to move blank space.
stats file is file including stats about solution:
  1st line - length of solution
  2nd line - number of visited nodes
  3rd line - number of proceeded nodes
  4th line - depth of solution
  5th line - time spend of finding solutions in ms.


Examples how to run program:
bfs RDLU input.txt output.txt stats.txt
dfs ULDR input.txt output.txt stats.txt
astr manh input.txt output.txt stats.txt
