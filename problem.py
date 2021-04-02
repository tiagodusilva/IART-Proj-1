from __future__ import annotations

import random
from math import exp
from decorators import timer
from copy import copy, deepcopy


class Library:
    """
    Represents and links all the information about a certain library
    """

    def __init__(self, n_books:int, signup:int, processing:int, id:int):
        self.n_books = n_books
        self.signup = signup
        self.processing = processing
        self.books = []
        self.id = id
    
    def __str__(self):
        return str(self.id)
    
    def __repr__(self):
        return str(self.id)
    
    def set_books(self, books:list):
        self.books = books


class Solution:
    
    def __init__(self, problem: Problem):
        super().__init__()
        self.problem = problem
        self.score = 0  # Smaller or equal estimate of the score (from eval)
        self.real_score = 0  # Best possible score (from get_useful_solution)

    @staticmethod
    def fromRandom(problem: Problem) -> Solution:
        """
        Generates a solution with random libraries order and random books order
        """
        self = Solution(problem)
        self.libraries = deepcopy(problem.libraries)
        random.shuffle(self.libraries)
        for lib in self.libraries:
            random.shuffle(lib.books)
        return self

    @staticmethod
    def fromRandomLibsOrderedBooks(problem: Problem) -> Solution:
        """
        Generates a solution with random libraries order and sorted books by score
        """
        self = Solution(problem)
        self.libraries = deepcopy(problem.libraries)
        random.shuffle(self.libraries)
        
        def sorting_key(book):
            return self.problem.scores[book]

        for lib in self.libraries:
            lib.books.sort(key=sorting_key, reverse=True)
        return self

    @staticmethod
    def fromGreedySearch(problem: Problem) -> Solution:
        """
        Generates a starting solution using a greedy algorithm
        """
        self = Solution(problem)
        self.libraries = deepcopy(problem.libraries)
        
        def book_sorting_key(book):
            return self.problem.scores[book] #Sorts the libraries by score in order to obrain the N first libraries still in the deadline

        for lib in self.libraries:
            lib.books.sort(key=book_sorting_key, reverse=True)
        
        def lib_sorting_key(lib):
            return sum(self.problem.scores[book] for book in lib.books) / lib.signup
        
        self.libraries.sort(key=lib_sorting_key, reverse=True)

        return self


    def getDeadLineLibs(self) -> list:
        """
        Returns the max index of the libraries still in the deadline.
        """
        t = 0
        index = 0
        for lib in self.libraries:
            t += lib.signup
            index += 1
            if t >= self.problem.deadline:
                break
        return index

    def swapLibs(self, index1:int=None, index2:int=None) -> (int, int):
        """
        Operator to swap two libraries. The index can be specified in order to use those or ommited in order to generate random indexes
        """
        if index1 == None:
            index1 = random.randrange(self.getDeadLineLibs())#guarentees the lib is in the deadline in order to make the change matter
        if index2 == None:
            index2 = random.randrange(len(self.libraries)) #gets the index of another random lib
            
        self.libraries[index1], self.libraries[index2] = self.libraries[index2], self.libraries[index1]
        return (index1, index2)

    def swapBooks(self, libIndex:int=None, indexBook1:int=None, indexBook2:int=None) -> (int, int, int):
        """
        Operator to swap two books. The index can be specified in order to use those or ommited in order to generate random indexes
        """
        if libIndex == None:
            libIndex = random.randrange(self.getDeadLineLibs()) #guarentees the lib is in the deadline in order to make the change matter
        if indexBook1 == None:
            indexBook1 = random.randrange(self.libraries[libIndex].n_books) #gets a random book to swap
        if indexBook2 == None:
            indexBook2 = random.randrange(self.libraries[libIndex].n_books)
            
        self.libraries[libIndex].books[indexBook1], self.libraries[libIndex].books[indexBook2] = (
            self.libraries[libIndex].books[indexBook2], 
            self.libraries[libIndex].books[indexBook1]
        ) #swaps the books
        return (libIndex, indexBook1, indexBook2)


    def __str__(self):
        return str(self.score)
    
    def __repr__(self):
        return str(self.score)


    def __xor__(self, other):
        return self.ox1(other)


    # Best Crossover operator
    def ox1(self, other: Solution) -> Solution:
        """
        Cross over operator for our genetic algorithm
        """
        #Obtains two indexes from a parent to cross over to the child all the libs between them
        left, right = random.randint(0, len(self.libraries)), random.randint(0, len(self.libraries)) 


        if right < left: #guarentees the order of the random indexes are correct
            right, left = left, right
        
        child_sol = Solution(self.problem)
        child_sol.libraries = [None for _ in self.libraries] #initiates a child with no libs

        for i in range(left, right): #copies the libraries in between the random indexes from the parent to the child
            child_sol.libraries[i] = deepcopy(other.libraries[i]) 
        
        #Copies the remaining libraries from the second parent to the child maintaining their order
        new_sol_i = right % len(child_sol.libraries)
        for i in range(len(child_sol.libraries)):
            j = (i + right) % len(child_sol.libraries) #in order to wrap the list so we can continuously iterate it (connects the tail to the head of the list)
            if self.libraries[j].id not in (lib.id for lib in child_sol.libraries if lib != None):
                child_sol.libraries[new_sol_i] = deepcopy(self.libraries[j])
                new_sol_i += 1
                if new_sol_i >= len(child_sol.libraries):
                    new_sol_i = 0

        return child_sol

    # First Crossover operator
    def singlePointCross(self, other: Solution) -> Solution:
        """
        The first cross over function
        """

        #Obtains one indexes from a parent to cross over to the child all the libs between it and the end
        left, right = random.randint(0, len(self.libraries)), len(self.libraries) 
        
        child_sol = Solution(self.problem)
        child_sol.libraries = [None for _ in self.libraries] #initiates a child with no libs

        for i in range(left, right): #copies the libraries in between the random index and the end from the parent to the child
            child_sol.libraries[i] = deepcopy(other.libraries[i]) 
        
        #Copies the remaining libraries from the second parent to the child maintaining their order
        j=0
        for i in range(0,right):
            if self.libraries[i].id not in (lib.id for lib in child_sol.libraries if lib != None):
                child_sol.libraries[j] = deepcopy(self.libraries[i])
                j+=1
                if(j>=right):
                    break

        return child_sol

    
    def __lt__(self, other):
        """
        Overload of the operator < in order to sort the libraries
        """
        if self.score == None:
            self.eval()
        if other.score == None:
            other.eval()
        return self.score < other.score


    def get_useful_solution(self) -> (list, list):

        books = set()
        libraries = []
        used_books = []
        t = 0
        for lib in self.libraries:
            t += lib.signup
            if t >= self.problem.deadline:  # once the libs are out of the deadline the function ends
                break
            
            tleft = max((self.problem.deadline - t, 0))
            max_books_scanned = min((lib.n_books, tleft * lib.processing))  # calculates how many books will be scanned from the lib

            lib_books = set()

            scanned = 0
            for b in lib.books:
                if scanned >= max_books_scanned:
                    break
                if b not in books:
                    scanned += 1
                    lib_books.add(b)
                    books.add(b)
            
            if len(lib_books) > 0:
                libraries.append(lib.id)
                used_books.append(lib_books)
            else:
                t -= lib.signup
    
        self.real_score = 0
        for book in books:
            self.real_score += self.problem.scores[book]
        
        return libraries, used_books


    def dump_solution(self, filename:str) -> None:
        """
        Dumps to a file the current solution in the format specified by the hashcode
        """
        outfile = open(filename, mode="w")

        libraries, used_books = self.get_useful_solution()

        outfile.write(f"{len(libraries)}")

        for i in range(len(libraries)):
            outfile.write(f"{libraries[i]} {len(used_books[i])}\n")
            for b in used_books[i]:
                outfile.write(f"{b} ")
            outfile.write(f"\n")

        outfile.close()


    def eval(self) -> int:
        """
        Evaluates the current solution taking into account the deadline and duplicate books
        """
        books = set()
        t = 0
        for lib in self.libraries:
            t += lib.signup
            if t >= self.problem.deadline:  # Once the libs are out of the deadline the function ends
                break

            tleft = max((self.problem.deadline - t, 0))
            max_books_scanned = min((lib.n_books, tleft * lib.processing))  # Calculates how many books will be scanned from the lib

            # Since we are using a set, if we try to insert a duplicate book, only one copy will remain
            books.update(lib.books[:max_books_scanned])

        self.score = 0
        for book in books:
            self.score += self.problem.scores[book]

        return self

 


class Problem:
    """
    Represents everything needed to represent and solve a book scanning problem
    """

    def __init__(self, n_books:int, n_libraries:int, deadline:int, scores:list, libraries:list, books:list, solution_initializer=Solution.fromRandom, verbose:bool=False):
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
    def from_file(filename:str, solution_initializer=Solution.fromRandom, verbose:bool=False) -> Problem:
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
    

    def neighborhood(self, solution:Solution):
        """
        Used in steepest ascend to calculate the neighborhood
        """
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
                    yield solution, ('sl', i, j) #similar to return, but restarts from here on the next call

                # Undo swap       
                t = prevT
                solution.swapLibs(index2, index1)
                solution.score = prevScore


    @timer
    def steepest_ascent(self) -> Solution:
        """
        Steepest Ascent is implemented however the time needed to complete is to long to be executed
        """
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
        return solution



    @timer
    def hill_climb(self) -> Solution:
        """
        The simple version of hill climbing is implemented.
        """
        solution = self.solution_initializer(self).eval()

        flag = True #controls the while loop for the hill climb

        while flag:
            t = 0
            for i in range(0, len(self.libraries)):
                t += solution.libraries[i].signup

                if t > self.deadline:
                    return solution

                for j in range(i + 1, len(self.libraries)):
      
                    prevScore = solution.score
                    index1, index2 = solution.swapLibs(i, j)
                    solution.eval()

                    prevT = t

                    #updates the time in accordance to the libs sawp
                    t = t - solution.libraries[index2].signup + solution.libraries[index1].signup 

                    if prevScore >= solution.score or t > self.deadline:
                        # Undo swap
                        t = prevT           
                        solution.swapLibs(index2, index1)
                        solution.score = prevScore
                    else:
                        had_better = True
                        if self.verbose:
                            print(f"Found better solution {solution.score} on the lib swap {index1} -> {index2}")

                if i == len(self.libraries) - 1: # if i is at the end, no more optimizations are possible and so the loop ends
                    return solution
                    
                if(t > self.deadline): #if we try to swap libraries that are out of the deadline, since it makes no difference we stop the loop
                    break


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
    def annealing(self, T:float, initial_cooling:float, final_cooling:float) -> Solution:
        solution = self.solution_initializer(self).eval()
        it = 0
        initial_T = T
        final_T = .1
        while T > final_T:

            it += 1
            # Linear Interpolation of cooling
            cooling = initial_cooling + (final_cooling - initial_cooling) * (T - initial_T) / (final_T - initial_T)
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
    def genetic(self, population:int, max_generations:int, mutation_chance:float, reproduce=Solution.singlePointCross) -> Solution:
        """
        Genetic algorithm with variable max generation and staring gens poll
        """
        parents = [Solution.fromRandom(self).eval() for i in range(population)] #generates the starting population
        half_population = population // 2
        generation = 0

        parents.sort(reverse=True) #sorts the generation's solution os the worse can be replaced by the children

        while generation < max_generations:
            children = copy(parents)

            for i in range(0, len(parents) // 2):
                father = parents[i]
                mother = random.choice(parents)

                children[i + half_population] = reproduce(father, mother) #creates a child and replaces a solution from the previous generation

                # Mutation
                if mutation_chance < random.random():
                    r = random.random()
                    if r > 0.2: # Switch Book
                        children[i + half_population].swapBooks()
                    else: # Switch Libraries
                        children[i + half_population].swapLibs()
                
                children[i + half_population].eval()
            
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
