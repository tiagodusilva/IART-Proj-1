import itertools
# from visualizer import plot_result


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

    def setIndex(self, index):
        self.index = index
    
    def set_books(self, books):
        self.books = books


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
        self.remaining_books = all_books
        self.scanned_books = set()

        for i in range(len(self.books)):
            self.books[i].sort(key=self.get_book_score, reverse=True)

        # Intermediate
        self.lib_evals = []

        # Solution
        self.libraries_used = []
        self.signups = []
        self.sent = []
        self.total_score = None
    

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
            self.sent.append(books_scanned)

            self.remaining_books.difference_update(books_scanned)

            self.scanned_books = self.scanned_books.union(books_scanned)

            curLibIndex += 1

        self.libraries_used = curLibIndex
        self.total_score = total_score

