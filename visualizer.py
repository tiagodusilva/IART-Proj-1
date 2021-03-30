import numpy as np
import matplotlib.pyplot as plt
from problem import Solution, Problem

def plot_result(sol, name="Hashcode Docs Example", show=False):
    """
    Plots the solution of a book scanning problem
    Not compatible with PyPy
    """

    p = sol.problem

    with plt.style.context('default'):

        # Create figure and axes
        fig = plt.figure("Book Scanning")
        ax = fig.subplots(1)
        ax.set_title(f"{name} ~ {sol.score}")

        total_scores = [sum(p.scores[b] for b in lib.books) for lib in p.libraries]
        scanned_scores = unique_lib_scores(sol)

        ax.bar(np.arange(0, len(p.libraries)), total_scores, color="green", alpha=0.1, label="Wasted potential score")
        ax.bar(np.arange(0, len(p.libraries)), scanned_scores, color="indigo", alpha=0.5, label="Score gained")

        ax.legend(loc="upper right")
        ax.set_xlabel("Library Index")
        ax.set_ylabel("Score")

        if show:
            plt.show()

        return fig, ax


def unique_lib_scores(sol: Solution):

    books = set()
    lib_scores = [0 for _ in sol.libraries]
    t = 0
    for i in range(len(sol.libraries)):
        lib = sol.libraries[i]
        t += lib.signup

        if t >= sol.problem.deadline:
            break
        
        lib_t = t
        processed = 0

        tleft = max((sol.problem.deadline - t, 0))
        max_books_scanned = min((lib.n_books, tleft * lib.processing))

        for b in lib.books[:max_books_scanned]:
            if b not in books:
                books.add(b)
                lib_scores[i] += sol.problem.scores[b]

    return lib_scores