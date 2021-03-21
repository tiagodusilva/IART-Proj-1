import numpy as np
import matplotlib.pyplot as plt

def plot_result(p, name="Hashcode Docs Example", show=False):

    with plt.style.context('default'):

        # Create figure and axes
        fig = plt.figure("Book Scanning")
        ax = fig.subplots(1)
        ax.set_title(f"{name} ~ {p.total_score}")

        total_scores = [sum(p.scores[b] for b in lib.books if b not in p.scanned_books) for lib in p.libraries]
        scanned_scores = [sum(p.scores[b] for b in lib.scanned) for lib in p.libraries]
        ax.bar(np.arange(0, len(total_scores)), total_scores, bottom=scanned_scores, color="green", alpha=0.1, label="Wasted potential score")
        ax.bar(np.arange(0, len(scanned_scores)), scanned_scores, color="indigo", alpha=0.5, label="Score gained")

        ax.legend(loc="upper right")
        ax.set_xlabel("Library Index")
        ax.set_ylabel("Score")

        if show:
            plt.show()

        return fig, ax
