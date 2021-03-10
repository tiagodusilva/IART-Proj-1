import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.patheffects as path_effects
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle


def plot_result(problem):
    
    with plt.style.context('seaborn-paper'):

        # Create figure and axes
        fig = plt.figure("Book Scanning")
        ax = fig.subplots(1)
        ax.set_title("Hashcode Docs Example")

        time = 0
        height = 0

        norm_scores = problem.scores / np.average(problem.scores)

        plot_deadline(ax, problem.deadline)
        cmap = plt.get_cmap("viridis")

        y_ticks = [0]

        for sign, books in zip(problem.signups, problem.sent):
            l = sign[0]
            signup_time = problem.libraries[l][1]
            parallel_books = problem.libraries[l][2]
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

        ax.set_xticks(np.arange(0, problem.deadline + 1, 1))
        ax.set_yticks(y_ticks)
        ax.grid(axis="x", alpha=.5, ls='--')
        ax.grid(axis="y", alpha=.5, ls='-')

        ax.set_xlim(-1, problem.deadline + 1)
        ax.set_ylim(0, height)

        ax.set_xlabel("Days")
        
        # ADD COLORMAP
        from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
        ax_divider = make_axes_locatable(ax)
        # Add an axes to the right of the main axes.
        cax = ax_divider.append_axes("right", size="5%", pad="5%", )
        norm = matplotlib.colors.Normalize(vmin=min(problem.scores), vmax=max(problem.scores))
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
