import numpy as np
import itertools
from visualizer import plot_result


class TestFiles:
    test_a = "test/a_example.txt"
    test_b = "test/b_read_on.txt"
    test_c = "test/c_incunabula.txt"
    test_d = "test/d_tough_choices.txt"
    test_e = "test/e_so_many_books.txt"
    test_f = "test/f_libraries_of_the_world.txt"


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
        self.all_books = all_books
        
        # Helpers
        self.pre_proc_scores = np.empty(n_libraries, dtype=float)
        self.aux_scores = scores
        self.signed_libraries = set()
        self.scanned_books = set()
        self.diff_books_amount = None

        # Solution
        self.libraries_used = None
        self.signups = None
        self.sent = None
        self.total_score = None
    
    @staticmethod
    def from_file(filename):
        with open(filename) as f:
            book, n_libraries, deadline = [int(elem) for elem in f.readline().split()]
            scores = np.array([int(elem) for elem in f.readline().split()])

            libraries = np.empty((n_libraries, 3), dtype=int)
            books = np.empty(n_libraries, dtype=object)
            all_books = np.empty(0, dtype=int)

            for i in range(n_libraries):
                libraries[i] = np.array([int(elem) for elem in f.readline().split()])
                books[i] = np.array([int(elem) for elem in f.readline().split()])
                all_books = np.append(all_books,books[i])
                

            return Problem(book, n_libraries, deadline, scores, libraries, books, all_books)
    
    def insert_test_sol(self):
        # Output data
        self.libraries_used = 2 # Two libraries will be signed up for scanning.
        self.signups = np.array([
            [1, 3], # The first library to do the signup process is library 1.
                    # After the sign up process it will send 3 books for scanning
            [0, 5]
        ])
        self.sent = np.array([
            [5, 2, 3], # Library 1 will send book 5, book 2, and book 3 in order.
            [0, 1, 2, 3, 4]
        ], dtype=object)

    def visualize(self, testfile):
        fig, ax = plot_result(self, testfile)
        # fig.savefig("uwu.png")


    def book_aux_score(self, book):
        return self.aux_scores[book]

    def eval_library(self, index):
        return sum(((self.aux_scores[i]*(1-self.diff_books_amount[i]/self.n_libraries)) for i in self.books[index])) / self.libraries[index][Problem.LIB_SIGNUP]
    
    
    #can be optimized
    def pre_proc(self):
        #gets the number  of times each book appears
        self.diff_books_amount = np.empty(len(self.aux_scores),dtype=int)

        for i in range(len(self.aux_scores)):
            self.diff_books_amount[i] = np.count_nonzero(self.all_books == i)
        
        
        for i in range(self.n_libraries):
            self.pre_proc_scores[i] = self.eval_library(i)

            

    def next_library(self, t):
        while(True):
            bestIndex = np.where(self.pre_proc_scores == np.amax(self.pre_proc_scores))[0][0]
            if(self.libraries[bestIndex][Problem.LIB_SIGNUP] + t < self.deadline or self.pre_proc_scores[bestIndex]==-1):
                return bestIndex
            else:
                self.pre_proc_scores[bestIndex] = -1;

    def hillclimbing(self):
        self.aux_scores = np.copy(self.scores)

        self.signups = []
        self.sent = []
        self.total_score = 0
        self.pre_proc()

        t = 0
        
        while t < self.deadline and len(self.signups) < self.n_libraries:
            nextLib = self.next_library(t)
            lib = self.libraries[nextLib]
            
            self.signups.append(nextLib)
            t += lib[Problem.LIB_SIGNUP]
            
            if(self.pre_proc_scores[nextLib] == -1):
                break

            tleft = max((self.deadline - t, 0))
            books_scanned = lib[Problem.LIB_BOOKS]
            if books_scanned > lib[Problem.LIB_PROCESSING]:
                books_scanned = min((lib[Problem.LIB_BOOKS], tleft * lib[Problem.LIB_PROCESSING]))

            books_to_use = self.books[nextLib]
            if books_scanned != lib[Problem.LIB_BOOKS]:
                books_to_use = sorted(self.books[nextLib], key=self.book_aux_score, reverse=True)
            lib_score = 0
            tmp_l = []
            for b in itertools.islice(books_to_use, books_scanned):
                lib_score += self.aux_scores[b]
                if (self.aux_scores[b] > 0):
                    tmp_l.append(b)
                self.aux_scores[b] = 0
                
            self.total_score += lib_score
            self.sent.append(np.array(tmp_l))
            
            self.pre_proc_scores[nextLib] = -1
