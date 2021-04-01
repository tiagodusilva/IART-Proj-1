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
    # General arguments
    parser.add_argument("-v", "--verbose", action = "count", help = "Increase verbosity")
    parser.add_argument("-t", "--test", action = "store", choices=testfiles.keys(), default="b", help = "Test file to use")
    parser.add_argument("-s", "--seed", action = "store", default=None, help = "Seed for the random generator")
    parser.add_argument("-p", "--plot", "--plotting", action = "store_true", help = "Plot result, incompatible with PyPy")
    parser.add_argument("-d", "--dump", action = "store_true", help = "Dumps the solution into the 'sol' directory")
    
    parser.add_argument("--hill", "--hillclimbing", action = "store_true", help = "Use hill climbing")
    
    # Simulated Annealing
    parser.add_argument("-sa", "--annealing", action = "store_true", help = "Use simulated annealing")
    parser.add_argument("-sat", "--annealing-temperature", action="store", nargs=1, type=float, default=[100000], help="Simulated annealing initial temperature")
    parser.add_argument("-saic", "--annealing-initial-cooling", action="store", nargs=1, type=float, default=[0.95], help="Simulated initial annealing cooling")
    parser.add_argument("-safc", "--annealing-final-cooling", action="store", nargs=1, type=float, default=[0.985], help="Simulated final annealing cooling")
    
    # Genetic
    parser.add_argument("-g", "--genetic", "--gen", action="store_true", help = "Use genetic algorithm")
    parser.add_argument("-gg", "--gen-generations", action="store", nargs=1, type=int, default=[100], help="Genetic algorithm ~ Number of generations")
    parser.add_argument("-gp", "--gen-population", action="store", nargs=1, type=int, default=[50], help="Genetic algorithm ~ Population size")
    parser.add_argument("-gm", "--gen-mutation-chance", action="store", nargs=1, type=float, default=[0.05], help="Genetic algorithm ~ Mutation chance")
    parser.add_argument("-g1pc", "--gen-one-point-crossover", action="store_true", help="Genetic algorithm ~ One point crossover operator")
    parser.add_argument("-g2pc", "--gen-two-point-crossover", action="store_true", help="Genetic algorithm ~ Two point crossover operator (OX1)")

    # Initial Solution
    parser.add_argument("-rs", "--random-start", action = "store_true", help = "Sets the inital solution to random")
    parser.add_argument("-os", "--ordered-start", action = "store_true", help = "Sets the inital solution to books ordered by score")
    parser.add_argument("-gs", "--greedy-start", action = "store_true", help = "Sets the inital solution to greedy search")


    args = parser.parse_args()

    # Unpack list arguments because they are annoying otherwise :)
    args.annealing_temperature = args.annealing_temperature[0]
    args.annealing_initial_cooling = args.annealing_initial_cooling[0]
    args.annealing_final_cooling = args.annealing_final_cooling[0]

    args.gen_generations = args.gen_generations[0]
    args.gen_population = args.gen_population[0]
    args.gen_mutation_chance = args.gen_mutation_chance[0]


    # Force an even population
    args.gen_population = (args.gen_population // 2) * 2

    args.testfile = testfiles[args.test]

    # Check for search mode, define default and check if multiple were specified
    search_modes = int(args.hill) + int(args.annealing) + int(args.genetic)
    if search_modes == 0:
        args.hill = True
    elif search_modes > 1:
        print("You cannot specify multiple search types at once!")
        exit()
    
    # Annealing cooling values check
    if args.annealing and (args.annealing_initial_cooling <= 0 or args.annealing_initial_cooling >= 1 or args.annealing_final_cooling <= 0 or args.annealing_final_cooling >= 1):
        print("The cooling parameters must be a floating value in the range ]0, 1[")
        exit()

    # Check for search start, define default and check if multiple were specified (ignored on genetic)
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
    

    # Check for genetic crossover operator, define default and check if multiple were specified
    crossover = int(args.gen_one_point_crossover) + int(args.gen_two_point_crossover)
    if crossover == 0:
        args.gen_one_point_crossover = True
    elif args.genetic and crossover > 1:
        print("You cannot specify multiple crossover operators at once!")
        exit()

    if args.gen_one_point_crossover:
        args.crossover_operator = Solution.singlePointCross
    else:
        args.crossover_operator = Solution.ox1

    # Verify if mutation chance is within the interval [0, 1]
    if args.genetic and args.gen_mutation_chance < 0 or args.gen_mutation_chance > 1:
        print("The mutation chance must be within the interval [0, 1]")
        exit()

    # Set seed if specified in the command
    if args.seed != None:
        random.seed(args.seed)

    return args
