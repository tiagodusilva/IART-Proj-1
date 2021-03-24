import sys
from problem import Problem
from args import parse_args

args = parse_args()

print(f"DATASET: {args.testfile}")
p = Problem.from_file(args.testfile, args.verbose)

if args.hill:
    sol = p.hill_climb()
    print(f"Hill Climbing Score: {sol.score}")
    pass
elif args.annealing:
    sol = p.annealing()
    print(f"Simulated Annealing Score: {sol.score}")
    pass
elif args.tabu:
    # sol = p.tabu_search()
    # print(f"Tabu Search Score: {sol.score}")
    pass
elif args.gen:
    sol = p.genetic()
    print(f"Genetic Score: {sol.score}")
    pass
else:
    print("Nani")
    exit()

# p.dump_solution(testfile.replace("test/", "sol/"))

if args.plot:
    from visualizer import plot_result
    import matplotlib.pyplot as plt

    # fig, ax = plot_result(p, testfile, show=True)
    # fig.savefig("uwu.png", dpi=200)
