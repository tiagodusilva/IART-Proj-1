import random
from math import exp
from decorators import timer
from copy import copy, deepcopy

class Library:
    """
    Represents and links all the information about a certain library
    """

    def __init__(self, n_books, signup, processing, id):
        self.n_books = n_books
        self.signup = signup
        self.processing = processing
        self.books = []
        self.id = id
    
    def __str__(self):
        return str(self.id)
    
    def __repr__(self):
        return str(self.id)
    
    def set_books(self, books):
        self.books = books


class Solution:
    
    def __init__(self, problem):
        super().__init__()
        self.problem = problem
        self.score = 0

    @staticmethod
    def fromRandom(problem):
        self = Solution(problem)
        self.libraries = deepcopy(problem.libraries)
        random.shuffle(self.libraries)
        for lib in self.libraries:
            random.shuffle(lib.books)
        return self

    @staticmethod
    def fromRandomLibsOrderedBooks(problem):
        self = Solution(problem)
        self.libraries = deepcopy(problem.libraries)
        random.shuffle(self.libraries)
        
        def sorting_key(book):
            return self.problem.scores[book]

        for lib in self.libraries:
            lib.books.sort(key=sorting_key, reverse=True)
        return self

    @staticmethod
    def fromGreedySearch(problem):
        self = Solution(problem)
        self.libraries = deepcopy(problem.libraries)
        
        def book_sorting_key(book):
            return self.problem.scores[book]

        for lib in self.libraries:
            lib.books.sort(key=book_sorting_key, reverse=True)
        
        def lib_sorting_key(lib):
            return sum(self.problem.scores[book] for book in lib.books) / lib.signup
        
        self.libraries.sort(key=lib_sorting_key, reverse=True)

        return self

    def getDeadLineBooks(self):
        t = 0
        index = 0
        for lib in self.libraries:
            t += lib.signup
            index += 1
            if t >= self.problem.deadline:
                break
        return self.libraries[:index]

    def swapLibs(self, index1=None, index2=None):
        if index1 == None:
            index1 = random.randrange(len(self.getDeadLineBooks()))
        if index2 == None:
            index2 = random.randrange(len(self.libraries))
            
        self.libraries[index1], self.libraries[index2] = self.libraries[index2], self.libraries[index1]
        return (index1, index2)

    def swapBooks(self, libIndex = None, indexBook1=None, indexBook2=None):
        if libIndex == None:
            libIndex = random.randrange(len(self.getDeadLineBooks()))
        if indexBook1 == None:
            indexBook1 = random.randrange(self.libraries[libIndex].n_books)
        if indexBook2 == None:
            indexBook2 = random.randrange(self.libraries[libIndex].n_books)
            
        self.libraries[libIndex].books[indexBook1], self.libraries[libIndex].books[indexBook2] = (
            self.libraries[libIndex].books[indexBook2], 
            self.libraries[libIndex].books[indexBook1]
        )
        return (libIndex, indexBook1, indexBook2)


    def __str__(self):
        return str(self.score)
    
    def __repr__(self):
        return str(self.score)


    def __xor__(self, other):
        return self.ox1(other)


    # Crossover operator
    def ox1(self, other):
        left, right = random.randint(0, len(self.libraries)), random.randint(0, len(self.libraries))
        if right < left:
            right, left = left, right
        
        child_sol = Solution(self.problem)
        child_sol.libraries = [None for _ in self.libraries]

        for i in range(left, right):
            child_sol.libraries[i] = deepcopy(other.libraries[i])
        
        new_sol_i = right % len(child_sol.libraries)
        for i in range(len(child_sol.libraries)):
            j = (i + right) % len(child_sol.libraries)
            if self.libraries[j].id not in (lib.id for lib in child_sol.libraries if lib != None):
                child_sol.libraries[new_sol_i] = deepcopy(self.libraries[j])
                new_sol_i += 1
                if new_sol_i >= len(child_sol.libraries):
                    new_sol_i = 0

        return child_sol

    
    def __lt__(self, other):
        if self.score == None:
            self.eval()
        if other.score == None:
            other.eval()
        return self.score < other.score


    def dump_solution(self, filename):
        """
        Dumps to a file the current solution in the format specified by the hashcode
        """
        outfile = open(filename, mode="w")

        outfile.write("uwu")

        # outfile.write(f"{self.libraries_used}\n")

        # for i in range(self.libraries_used):
        #     outfile.write(f"{self.signups[i].index} {len(self.sent[i])}\n")
        #     for b in self.sent[i]:
        #         outfile.write(f"{b} ")
        #     outfile.write(f"\n")

        outfile.close()


    def eval(self):
        
        books = set()
        t = 0
        for lib in self.libraries:
            t += lib.signup
            if t >= self.problem.deadline:
                break
            
            lib_t = t
            processed = 0

            tleft = max((self.problem.deadline - t, 0))
            max_books_scanned = min((lib.n_books, tleft * lib.processing))

            books.update(lib.books[:max_books_scanned])

        self.score = 0
        for book in books:
            self.score += self.problem.scores[book]

        return self

 


class Problem:
    """
    Represents everything needed to represent and solve a book scanning problem
    """

    def __init__(self, n_books, n_libraries, deadline, scores, libraries, books, solution_initializer=Solution.fromRandom, verbose=False):
        super().__init__()
        # Input
        self.n_books = n_books
        self.n_libraries = n_libraries
        self.deadline = deadline
        self.scores = scores
        self.libraries = libraries
        self.books = books
        self.solution_initializer = solution_initializer
        self.verbose = verbose


    @staticmethod
    @timer
    def from_file(filename, solution_initializer=Solution.fromRandom, verbose=False):
        """
        Returns a new problem from a given input file
        """
        with open(filename) as f:
            n_books, n_libraries, deadline = [int(elem) for elem in f.readline().split()]
            scores = list([int(elem) for elem in f.readline().split()])

            libraries = []
            books = []

            for i in range(n_libraries):
                libraries.append(Library(*(int(elem) for elem in f.readline().split()), i))
                books.append([int(elem) for elem in f.readline().split()])
                libraries[i].set_books(books[-1])

            return Problem(n_books, n_libraries, deadline, scores, libraries, books, solution_initializer, verbose)
    

    def neighborhood(self, solution):
        t = 0
        for i in range(0, len(self.libraries)):
            t += self.libraries[i].signup

            for j in range(i + 1, len(self.libraries)):

                # if t > self.deadline:
                #     continue

                prevScore = solution.score
                index1, index2 = solution.swapLibs(i, j)

                prevT = t
                t = t - self.libraries[index2].signup + self.libraries[index1].signup

                if t < self.deadline:
                    solution.eval()
                    yield solution, ('sl', i, j)

                # Undo swap       
                t = prevT
                solution.swapLibs(index2, index1)
                solution.score = prevScore


    @timer
    def steepest_ascent(self):
        solution = self.solution_initializer(self).eval()

        while True:
            prevScore = solution.score
            best_op = None
            for sol, op in self.neighborhood(solution):
                if sol.score > prevScore:
                    best_op = op
            
            if best_op == None:
                return solution

            solution.swapLibs(best_op[1], best_op[2])
            solution.eval()

            if self.verbose:
                print(f"Best neighbour: {sol.score} -------- Op: {best_op}")


    @timer
    def hill_climb(self):
        solution = self.solution_initializer(self).eval()

        flag = True
        nextIter = False
        while flag:
            t=0
            for i in range(0, len(self.libraries)):
                t+=self.libraries[i].signup

                for j in range(i + 1, len(self.libraries)):
                    # print(j)

                    prevScore = solution.score
                    index1, index2 = solution.swapLibs(i, j)
                    solution.eval()

                    prevT = t
                    t = t - self.libraries[index2].signup + self.libraries[index1].signup

                    if prevScore >= solution.score or t > self.deadline:
                        # Undo swap       
                        t = prevT           
                        solution.swapLibs(index2, index1)
                        solution.score = prevScore
                    else:
                        
                        if self.verbose:
                            print(f"Found better solution {solution.score} on the lib swap {index1} -> {index2}")
                if i == len(self.libraries) - 1:
                    flag = False
                if nextIter:
                    nextIter = False 
                    break
                if(t > self.deadline):
                    flag=False
                    break
        
        return solution

#         Pseudocode
# algorithm Discrete Space Hill Climbing is
#     currentNode := startNode
#     loop do
#         L := NEIGHBORS(currentNode)
#         nextEval := −INF
#         nextNode := NULL
#         for all x in L do
#             if EVAL(x) > nextEval then
#                 nextNode := x
#                 nextEval := EVAL(x)
#         if nextEval ≤ EVAL(currentNode) then
#             // Return current node since no better neighbors exist
#             return currentNode
#         currentNode := nextNode

    @timer
    def annealing(self, T, cooling):
        solution = self.solution_initializer(self).eval()
        iteraciones = []
        it = 0
        while T > .1:

            it += 1
            T *= cooling

            prevScore = solution.score

            r = random.random()
            op = None
            if r > 0.5: # Switch Book
                op = solution.swapBooks()
            else: # Switch Libraries
                op = solution.swapLibs()
            
            solution.eval()
            delta = solution.score - prevScore
            # Reversed conditions as we want to "go back" as our "stay in the current state"
            if delta >= 0:
                if self.verbose:
                    print(f"BEST: {solution.score}")
            else:
                exp_arg = delta / T
                if exp_arg < -2000 or exp(exp_arg) < random.random():
                    # Undo operation
                    if r > 0.5: # Switch Book
                        solution.swapBooks(*op)
                    else: # Switch Libraries
                        solution.swapLibs(*op)
                    solution.score = prevScore

            iteraciones.append((T, solution.score))
            # print(f"Temp: {T}")
        f = open("iteraciones.txt", 'w')
        for T, _ in iteraciones:
            f.write(f'{T} ')
        f.write('\n')
        for _, s in iteraciones:
            f.write(f'{s} ')
        f.close()
        if(self.verbose):
            print("Iterations:", it)
        return solution

    #         Pseudocode
    # Let s = s0
    # For k = 0 through kmax (exclusive):
    #     T ← temperature( (k+1)/kmax )
    #     Pick a random neighbour, snew ← neighbour(s)
    #     If P(E(s), E(snew), T) ≥ random(0, 1):
    #         s ← snew
    # Output: the final state s

    @timer
    def genetic(self, population, max_generations, reproduce = Solution.ox1):
        parents = [Solution.fromRandom(self).eval() for i in range(population)]
        half_population = 25
        generation = 0

        while generation < max_generations:
            parents.sort(reverse=True)
            children = copy(parents)

            for i in range(0, len(parents) // 2):
                father = parents[i]
                mother = random.choice(parents)

                children[i + half_population] = reproduce(father, mother).eval()

                # Mutation
                if 0.05 < random.random():
                    r = random.random()
                    if r > 0.2: # Switch Book
                        children[i + half_population].swapBooks()
                    else: # Switch Libraries
                        children[i + half_population].swapLibs()
            
            # Sort list by libraries scores
            parents = children
            parents.sort(reverse=True)

            generation += 1

            # Swaps the worst half of the parent for the best half of the children
            if self.verbose:
                print(f"Gen {generation} best and worst: {parents[0]} | {parents[-1]}")
        
            # for j in range(0,len(parents)//2):
            #     parents[len(parents) // 2 + j] = children[j]
    
        return parents[0]
