import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.patheffects as path_effects
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

plt.style.use('seaborn-paper')

# Input data
n_books, n_libraries, deadline = 6, 2, 7
scores = np.array([1, 2, 3, 6, 5, 4])

library = np.array([
    [5, 2, 2], # Library 0 has 5 books, the sign up process takes 2 days, and the library can ship 2 books per day.
    [4, 3, 1]
])

book = np.array([
    [0, 1, 2, 3, 4], # The books in library 0 are: book0, book1, book2, book3, and book4.
    [3, 2, 5, 0]
], dtype=object)



# Output data
libraries_used = 2 # Two libraries will be signed up for scanning.
signups = np.array([
    [1, 3], # The first library to do the signup process is library 1.
            # After the sign up process it will send 3 books for scanning
    [0, 5]
])
sent = np.array([
    [5, 2, 3], # Library 1 will send book 5, book 2, and book 3 in order.
    [0, 1, 2, 3, 4]
], dtype=object)


def plot_result(n_books, n_libraries, deadline, scores, library, book, signups, sent):

    # Create figure and axes
    fig = plt.figure("Book Scanning")
    ax = fig.subplots(1)
    ax.set_title("Hashcode Docs Example")

    time = 0
    height = 0

    norm_scores = scores / np.average(scores)

    plot_deadline(ax, deadline)
    cmap = plt.get_cmap("viridis")

    y_ticks = [0]

    for sign, books in zip(signups, sent):
        l = sign[0]
        signup_time = library[l][1]
        parallel_books = library[l][2]
        library_height = min((parallel_books, len(books)))
        y_ticks.append(y_ticks[-1] + library_height)
        
        plot_signup(ax, l, time, height, library_height, signup_time)
        time += signup_time
        
        booktime = time
        bpd = 0 # Books per day
        for b in books:
            plot_book(ax, b, booktime, height + bpd, c=cmap(norm_scores[b]))
            bpd += 1
            if (bpd >= parallel_books):
                bpd = 0
                booktime += 1

        height += library_height

    ax.set_xticks(np.arange(0, deadline + 1, 1))
    ax.set_yticks(y_ticks)
    ax.grid(axis="x", alpha=.5, ls='--')
    ax.grid(axis="y", alpha=.5, ls='-')

    ax.set_xlim(-1, deadline + 1)
    ax.set_ylim(0, height)

    ax.set_xlabel("Days")
    
    # ADD COLORMAP
    from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
    ax_divider = make_axes_locatable(ax)
    # Add an axes to the right of the main axes.
    cax = ax_divider.append_axes("right", size="5%", pad="5%", )
    norm = matplotlib.colors.Normalize(vmin=min(scores), vmax=max(scores))
    fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation='vertical')
    cax.set_ylabel("Score")
    

    return fig, ax



def plot_book(ax, book, day, y, d=0.5, h=0.5, c="pink"):
    rect = Rectangle((day + 0.25, y + 0.5 - h / 2), d, h, facecolor=c, edgecolor='k', lw=0.5)
    ax.add_patch(rect)
    text = ax.text(day + 0.5, y + 0.5, book, ha="center", va="center", c="w", clip_on=True)
    text.set_path_effects([path_effects.Stroke(linewidth=1, foreground='black'), path_effects.Normal()])

def plot_signup(ax, library, day, y, library_height, duration, h=0.25):
    rect = Rectangle((day, y + library_height / 2 - h / 2), duration, h, facecolor="#CFE2F3", edgecolor='k', lw=0.5)
    ax.add_patch(rect)
    ax.text(day + duration / 2, y + library_height / 2, f"Lib {library}", ha="center", va="center", clip_on=True)
    ax.text(-0.5, y + library_height / 2, f"Lib {library}", ha="center", va="center", clip_on=True)

def plot_deadline(ax, deadline):
    ax.vlines(deadline, 0, 100, colors='r')



fig, ax = plot_result(n_books, n_libraries, deadline, scores, library, book, signups, sent)
plt.show()

# fig.savefig("Book Scanning Demo.png")
