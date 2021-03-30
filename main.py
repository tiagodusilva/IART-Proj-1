import sys
from problem import Problem
from problem import Solution
from args import parse_args

args = parse_args()

print(f"DATASET: {args.testfile}")
p = Problem.from_file(args.testfile, args.solution_initializer, args.verbose)

sol = None
if args.hill:
    sol = p.hill_climb()
    print(f"Hill Climbing Score: \t\t{sol.score}")
elif args.annealing:
    sol = p.annealing(T=args.annealing_temperature, initial_cooling=args.annealing_initial_cooling, final_cooling=args.annealing_final_cooling)
    print(f"Simulated Annealing Score: \t{sol.score}")
elif args.gen:
    sol = p.genetic(population=args.gen_population, max_generations=args.gen_generations)
    print(f"Genetic Score: \t\t\t{sol.score}")

sol.get_useful_solution()
print(f"Real Score: \t\t\t{sol.score}")

if args.dump:
    dumpfile = args.testfile.replace("test/", "sol/")
    sol.dump_solution(dumpfile)
    print(f"Wrote solution to {dumpfile}")

if args.plot:
    from visualizer import plot_result
    import matplotlib.pyplot as plt

    fig, ax = plot_result(sol, args.testfile, show=True)
    fig.savefig("uwu.png", dpi=200)
