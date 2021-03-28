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
    parser.add_argument("-sa", "--annealing", action = "store_true", help = "Use simulated annealing")
    parser.add_argument("-g", "--gen", "--genetic", action = "store_true", help = "Use genetic algorithm")
    parser.add_argument("-r", "--random", action = "store_true", help = "Randomize the book order")

    args = parser.parse_args()

    args.testfile = testfiles[args.test]
    search_modes = int(args.hill) + int(args.annealing) + int(args.gen)

    if search_modes == 0:
        args.hill = True
    elif search_modes > 1:
        print("You cannot specify multiple search types at once!")
        exit()
    
    random.seed(args.seed)

    return args
