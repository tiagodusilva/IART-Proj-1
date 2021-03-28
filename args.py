from problem import Solution
import argparse
import random

testfiles = {
    "a": "test/a_example.txt",
    "b": "test/b_read_on.txt",
    "c": "test/c_incunabula.txt",
    "d": "test/d_tough_choices.txt",
    "e": "test/e_so_many_books.txt",
    "f": "test/f_libraries_of_the_world.txt"
}

def parse_args():
    parser = argparse.ArgumentParser(description = "Book Scanning ~ IART Proj 1 g42")
    parser.add_argument("-v", "--verbose", action = "count", help = "Increase verbosity")
    parser.add_argument("-t", "--test", action = "store", choices=testfiles.keys(), default="b", help = "Test file to use")
    parser.add_argument("-s", "--seed", action = "store", default=None, help = "Seed for the random generator")
    parser.add_argument("-p", "--plot", "--plotting", action = "store_true", help = "Plot result, incompatible with PyPy")
    
    parser.add_argument("--hill", "--hillclimbing", action = "store_true", help = "Use hill climbing")
    
    # Simulated Annealing
    parser.add_argument("-sa", "--annealing", action = "store_true", help = "Use simulated annealing")
    parser.add_argument("-sat", "--annealing-temperature", action="store", nargs=1, type=float, default=1000000, help="Simulated annealing initial temperature")
    parser.add_argument("-sac", "--annealing-cooling", action="store", nargs=1, type=float, default=0.9, help="Simulated annealing cooling")
    
    # Genetic
    parser.add_argument("-g", "--gen", "--genetic", action="store_true", help = "Use genetic algorithm")
    parser.add_argument("-gg", "--gen-generations", action="store", nargs=1, type=int, default=100, help="Genetic algorithm ~ Number of generations")
    parser.add_argument("-gp", "--gen-population", action="store", nargs=1, type=int, default=50, help="Genetic algorithm ~ Population size")

    # Initial Solution
    parser.add_argument("-rs", "--random-start", action = "store_true", help = "Sets the inital solution to random")
    parser.add_argument("-os", "--ordered-start", action = "store_true", help = "Sets the inital solution to books ordered by score")
    parser.add_argument("-gs", "--greedy-start", action = "store_true", help = "Sets the inital solution to greedy search")

    args = parser.parse_args()
    
    # Force an even population
    args.gen_population = (args.gen_population // 2) * 2

    args.testfile = testfiles[args.test]
    search_modes = int(args.hill) + int(args.annealing) + int(args.gen)

    if search_modes == 0:
        args.hill = True
    elif search_modes > 1:
        print("You cannot specify multiple search types at once!")
        exit()
    
    search_starts = int(args.random_start) + int(args.ordered_start) + int(args.greedy_start)

    if search_starts == 0:
        args.random_start = True
    elif search_modes > 1 and not args.genetic:
        print("You cannot specify multiple search starts at once!")
        exit()
    
    if args.random_start:
        args.solution_initializer = Solution.fromRandom
    elif args.ordered_start:
        args.solution_initializer = Solution.fromRandomLibsOrderedBooks
    else: args.solution_initializer = Solution.fromGreedySearch
    
    random.seed(args.seed)

    return args
