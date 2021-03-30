import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn')

fig = plt.figure()
axs = fig.subplots(2, 1)


times = {
    'hillclimb': {
        'b': [18.433037996292114, 18.228569984436035, 21.56929898262024, 16.3922278881073, 15.825484037399292],
        'e': [83.57326602935791, 79.71586894989014, 80.75503087043762],
        'f': [1.1457018852233887, 1.5012421607971191, 1.1962449550628662],
    },
    'genetic': {
        'b': [34.58673715591431, 30.035337924957275, 29.390383005142212],
        'e': [103.24016094207764, 103.91299200057983, 105.62652802467346],
        'f': [125.81935095787048, 125.31872797012329, 126.56094288825989],
    },
    'annealing': {
        'b': [3.026703119277954, 3.386115074157715, 3.2145931720733643],
        'e': [105.62652802467346, 103.91299200057983, 103.24016094207764],
        'f': [0.49098706245422363, 0.5196659564971924, 0.5149869918823242],
    }
}

scores = {
    'hillclimb': {
        'b': [5766200, 5702400, 5694000, 5735900, 5588000],
        'e': [2885225, 2831406, 2849203],
        'f': [2014381, 2080571, 1869776],
    },
    'genetic': {
        'b': [4836500, 4830700, 5094400],
        'e': [994063, 1115685, 1020149],
        'f': [2048876, 2367734, 1979183],
    },
    'annealing': {
        'b': [5472700, 5541200, 5581800],
        'e': [2831406, 2849203, 2885225],
        'f': [3335864, 3431130, 3435196],
    }
}

def extract_data(data, key):
    return [np.mean(val) for val in data[key].values()]

score_hist = axs[0]

w = 0.2
labels = ['B', 'F']
x = np.arange(len(labels))

score_hist.bar(x - w, extract_data(scores, 'hillclimb'), w, label='hillclimb', alpha=.75)
score_hist.bar(x, extract_data(scores, 'annealing'), w, label='annealing', alpha=.75)
score_hist.bar(x + w, extract_data(scores, 'genetic'), w, label='genetic', alpha=.75)

score_hist.set_ylabel('Scores')
score_hist.set_title('Score by Dataset')
score_hist.set_xticks(x)
score_hist.set_xticklabels(labels)
score_hist.legend(loc="upper center")

time_hist = axs[1]

time_hist.bar(x - w, extract_data(times, 'hillclimb'), w, label='hillclimb', alpha=.75)
time_hist.bar(x, extract_data(times, 'annealing'), w, label='annealing', alpha=.75)
time_hist.bar(x + w, extract_data(times, 'genetic'), w, label='genetic', alpha=.75)

time_hist.set_ylabel('Time')
time_hist.set_title('Execution time by Dataset')
time_hist.set_xticks(x)
time_hist.set_xticklabels(labels)
time_hist.legend(loc="upper center")

fig.tight_layout()

fig.savefig('dataset_score.png')
plt.show()

