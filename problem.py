import numpy as np
import matplotlib.pyplot as plt
from visualizer import plot_result

class TestFiles:
    test_a = "test/a_example.txt"
    test_b = "test/b_read_on.txt"
    test_c = "test/c_incunabula.txt"
    test_d = "test/d_tough_choices.txt"
    test_e = "test/e_so_many_books.txt"
    test_f = "test/f_libraries_of_the_world.txt"


class Problem:

    def __init__(self, n_books, n_libraries, deadline, scores, libraries, books):
        super().__init__()
        self.n_books = n_books
        self.n_libraries = n_libraries
        self.deadline = deadline
        self.scores = scores
        self.libraries = libraries
        self.books = books
        
        self.libraries_used = None
        self.signups = None
        self.sent = None
    
    @staticmethod
    def from_file(str):
        with open("test/a_example.txt") as f:
            book, n_libraries, deadline = [int(elem) for elem in f.readline().split()]
            scores = np.array([int(elem) for elem in f.readline().split()])

            libraries = np.empty((n_libraries, 3), dtype=int)
            books = np.empty(n_libraries, dtype=object)

            for i in range(n_libraries):
                libraries[i] = np.array([int(elem) for elem in f.readline().split()])
                books[i] = np.array([int(elem) for elem in f.readline().split()])


            return Problem(book, n_libraries, deadline, scores, libraries, books)
    
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

    def visualize(self):
        fig, ax = plot_result(self)
        fig.savefig("uwu.png")





