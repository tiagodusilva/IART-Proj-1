import random
from math import exp

class TestFiles:
    test_a = "test/a_example.txt"
    test_b = "test/b_read_on.txt"
    test_c = "test/c_incunabula.txt"
    test_d = "test/d_tough_choices.txt"
    test_e = "test/e_so_many_books.txt"
    test_f = "test/f_libraries_of_the_world.txt"

class Library:

    def __init__(self, index, n_books, signup, processing):
        self.index = index
        self.n_books = n_books
        self.signup = signup
        self.processing = processing
        self.books = None
        self.scanned = None
    
    def __str__(self):
        return str(self.index)
    
    def __repr__(self):
        return str(self.index)

    def setIndex(self, index):
        self.index = index
    
    def set_books(self, books):
        self.books = books
    
    def set_scanned(self, scanned):
        self.scanned = scanned



class Problem:

    # Library indexes
    LIB_BOOKS = 0
    LIB_SIGNUP = 1
    LIB_PROCESSING = 2

    def __init__(self, n_books, n_libraries, deadline, scores, libraries, books, all_books):
        super().__init__()
        # Input
        self.n_books = n_books
        self.n_libraries = n_libraries
        self.deadline = deadline
        self.scores = scores
        self.libraries = libraries
        self.books = books

        self.unused_libraries = []
        self.remaining_books = all_books
        self.scanned_books = set()
        self.time_left = None

        for i in range(len(self.books)):
            self.books[i].sort(key=self.get_book_score, reverse=True)

        # Intermediate
        self.lib_evals = []

        # Solution
        self.libraries_used = []
        self.signups = []
        self.sent = []
        self.total_score = None
    
        # Methods
        self.operations = []


    @staticmethod
    def from_file(filename):
        with open(filename) as f:
            book, n_libraries, deadline = [int(elem) for elem in f.readline().split()]
            scores = list([int(elem) for elem in f.readline().split()])

            libraries = []
            books = []
            all_books = set()

            for i in range(n_libraries):
                libraries.append(Library(i, *(int(elem) for elem in f.readline().split())))
                books.append([int(elem) for elem in f.readline().split()])
                libraries[i].set_books(books[-1])
                all_books = all_books.union(books[-1])

            return Problem(book, n_libraries, deadline, scores, libraries, books, all_books)

    def get_book_score(self, book):
        return self.scores[book]

    def dump_solution(self, filename):
        outfile = open(filename, mode="w")

        outfile.write(f"{self.libraries_used}\n")

        for i in range(self.libraries_used):
            outfile.write(f"{self.signups[i].index} {len(self.sent[i])}\n")
            for b in self.sent[i]:
                outfile.write(f"{b} ")
            outfile.write(f"\n")

        outfile.close()
    
    def get_unused_libraries(self):
        self.unused_libraries = [lib for lib in self.libraries if lib not in self.signups]


    def eval_libs(self):
        self.lib_evals = [self.eval_library_index(l.index) for l in self.libraries]

    def eval_library_index(self, index):
        return sum((self.scores[i] for i in self.books[index])) / self.libraries[index].signup

    def eval_library(self, library):
        return self.eval_library_index(library.index)

    def hillclimbing_fast(self):
        self.signups = []
        self.sent = []

        self.eval_libs()

        libs = sorted(self.libraries, key=self.eval_library, reverse=True)
        total_score = 0

        t = 0
        curLibIndex = 0
        while curLibIndex < self.n_libraries:
            curLib = libs[curLibIndex]
            t += curLib.signup
            if t >= self.deadline:
                break
            
            self.time_left = self.deadline - t
            self.signups.append(curLib)
            
            tleft = max((self.deadline - t, 0))
            max_books_scanned = min((curLib.n_books, tleft * curLib.processing))

            books_scanned = set()
            n_books_scanned = 0
            for book in curLib.books:
                if n_books_scanned >= max_books_scanned:
                    break
                if book not in self.scanned_books:
                    books_scanned.add(book)
                    n_books_scanned += 1
                    total_score += self.scores[book]
            curLib.set_scanned(books_scanned)
            self.sent.append(books_scanned)

            self.remaining_books.difference_update(books_scanned)
            self.scanned_books.update(books_scanned)

            curLibIndex += 1

        self.libraries_used = curLibIndex
        self.total_score = total_score

        chosen_lib_books = set()
        for l in self.signups:
            chosen_lib_books.update(l.books)
        self.remaining_books.intersection_update(chosen_lib_books)

        self.get_unused_libraries()

    # def operator_switch_library(self):
    #     lib = random.choice(self.unused_libraries)

    #     try:
    #         lib_to_replace = random.choice((l for l in self.signups if lib.signup <= self.time_left + l.signup))
    #     except IndexError:
    #         return None

    def undo(self):
        op = self.operations.pop()

        if op[0] == 'sb':
            # Switch book
            _, lib, book, book_to_replace = op

            # print("It's rewind time")

            lib.scanned.add(book_to_replace)
            lib.scanned.remove(book)
            self.remaining_books.add(book)
            self.remaining_books.remove(book_to_replace)
            self.total_score -= self.scores[book] - self.scores[book_to_replace]
        else:
            raise RuntimeError()
    
    def apply_operator(self, op):
        if op[0] == 'sb':
            self.operator_switch_book(*op[1:])
        else:
            raise RuntimeError()
    
    def operator_switch_book(self, lib=None, book=None, book_to_replace=None):
        if book == None or lib == None or book_to_replace == None:
            book = random.choice(tuple(self.remaining_books))

            try:
                lib = random.choice([l for l in self.signups if book in l.books])
            except:
                return False
            
            # TODO: Implement trying to readd the book into another library
            book_to_replace = random.choice(tuple(lib.scanned))


        lib.scanned.remove(book_to_replace)
        lib.scanned.add(book)
        self.remaining_books.add(book_to_replace)
        self.remaining_books.remove(book)

        self.total_score += self.scores[book] - self.scores[book_to_replace]
        self.operations.append(("sb", lib, book, book_to_replace))

        return True

    def annealing(self):
        
        T = 20
        while True:
            if len(self.remaining_books) == 0:
                return
            T *= 0.99
            old_score = self.total_score
            while not self.operator_switch_book():
                pass
            delta = self.total_score - old_score
            # Reversed conditions as we want to "fuck go back" as our "stay in the current state"
            # if delta <= 0 and exp(delta / T) < random.uniform(0, 1):
            #     self.undo()
            if delta > 0:
                print(f"BEST: {self.total_score}")
                # print(self.sent)
            elif exp(delta / T) < random.uniform(0, 1):
                self.undo()



    def get_best_operator(self):
        best_op_score = -1
        best_op = None

        for book in self.remaining_books:
            for lib in self.signups:
                if book in lib.books:
                    for book_to_replace in lib.scanned:
                        op_score = self.total_score + self.scores[book] - self.scores[book_to_replace]
                        # Pode dar asneira, check later
                        if op_score > best_op_score and ("sb", lib, book, book_to_replace) not in self.tabu_list:
                            best_op = ("sb", lib, book, book_to_replace)
                            best_op_score = op_score

        if best_op == None:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

        return best_op, best_op_score


    def tabu_search(self):
        self.tabu_list = []

        while (True): # Stop condition
            op, op_score = self.get_best_operator()

            if op_score > self.total_score:
                # Go to state
                self.apply_operator(op)
                print("UWU UWU UWU UWU")
                pass
            else:
                print("RRRRRREEEEEEEEEEEEEEE")
            
            self.tabu_list.append(op)
            if len(self.tabu_list) > 100: # Max size of tabu list
                del self.tabu_list[0]
        
        return self.total_score
