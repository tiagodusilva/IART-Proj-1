import numpy as np
import matplotlib.pyplot as plt


import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn')

fig = plt.figure()
gs = fig.add_gridspec(3, 1,)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1:, 0])

def get_data(filename):
    f = open(filename, 'r')
    T = [float(val) for val in f.readline().split()]
    scores = [int(val) for val in f.readline().split()]
    return {
        'T': T,
        'score': scores
    }

data = {
    'rs': get_data('d_random_start.txt'),
    'os': get_data('d_ordered_start.txt'),
    'gs': get_data('d_greedy_start.txt'),
    # 'oof': get_data('../iteraciones.txt'),
}

ax1.plot(data['gs']['T'], data['gs']['score'], label='Greedy Start', marker=".", c="#EE00FF", ms=.1)
# ax.plot(data['oof']['T'], data['oof']['score'], label='Latest Run', marker=".")

ax1.set_ylabel('Score')
ax1.invert_xaxis()
ax1.legend()
ax1.set_title('Score per iteration of Simulated Annealing')

ax2.plot(data['rs']['T'], data['rs']['score'], label='Random Start', marker=".", ms=.1)
ax2.plot(data['os']['T'], data['os']['score'], label='Ordered Start', marker=".", ms=.1)

ax2.set_xlabel('Temperature')
ax2.set_ylabel('Score')
ax2.invert_xaxis()
ax2.legend()

fig.tight_layout()

fig.savefig('iterations.png')
plt.show()

