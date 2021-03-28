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
    print(f"Hill Climbing Score: {sol.score}")
elif args.annealing:
    sol = p.annealing(T=args.annealing_temperature, cooling=args.annealing_cooling)
    print(f"Simulated Annealing Score: {sol.score}")
elif args.gen:
    sol = p.genetic(population=args.gen_population, max_generations=args.gen_generations)
    print(f"Genetic Score: {sol.score}")

# p.dump_solution(testfile.replace("test/", "sol/"))

if args.plot:
    from visualizer import plot_result
    import matplotlib.pyplot as plt

    fig, ax = plot_result(sol, args.testfile, show=True)
    fig.savefig("uwu.png", dpi=200)
