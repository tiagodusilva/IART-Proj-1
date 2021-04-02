import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn')

fig = plt.figure()
axs = fig.subplots(2, 1)


times = {
    'hillclimb': {
        'b': [18.433037996292114, 18.228569984436035, 21.56929898262024, 16.3922278881073, 15.825484037399292],
        'c': [698.9104669094086, 672.6828520298004, 672.4158980846405],
        'e': [83.57326602935791, 79.71586894989014, 80.75503087043762],
        'f': [1.1457018852233887, 1.5012421607971191, 1.1962449550628662],
    },
    'genetic': {
        'b': [34.58673715591431, 30.035337924957275, 29.390383005142212],
        'c': [1228.0823121070862, 1215.7536449432373, 1230.9619481563568],
        'e': [103.24016094207764, 103.91299200057983, 105.62652802467346],
        'f': [125.81935095787048, 125.31872797012329, 126.56094288825989],
    },
    'annealing rs': {
        'b': [3.026703119277954, 3.386115074157715, 3.2145931720733643],
        'c': [0.40021491050720215, 0.4038259983062744, 0.39359593391418457],
        'e': [0.6259291172027588, 0.6351079940795898, 0.6470639705657959],
        'f': [0.49098706245422363, 0.5196659564971924, 0.5149869918823242],
    },
    'annealing gs': {
        'b': [2.9388749599456787, 3.0284500122070312, 2.9869210720062256],
        'c': [1.3600568771362305, 1.3616337776184082, 1.405686855316162],
        'e': [1.3402838706970215, 1.333543062210083, 1.367056131362915],
        'f': [1.0113999843597412, 0.9845149517059326, 1.0045998096466064],
    },
}

scores = {
    'hillclimb': {
        'b': [5766200, 5702400, 5694000, 5735900, 5588000],
        'c': [1987935, 1939654, 1977192],
        'e': [2885225, 2831406, 2849203],
        'f': [2014381, 2080571, 1869776],
    },
    'genetic': {
        'b': [4836500, 4830700, 5094400],
        'c': [1103240, 1171043, 1086709],
        'e': [994063, 1115685, 1020149],
        'f': [2048876, 2367734, 1979183],
    },
    'annealing rs': {
        'b': [5472700, 5541200, 5581800],
        'c': [1264497, 1223781, 1164575],
        'e': [1732760, 1731381, 1774949],
        'f': [3335864, 3431130, 3435196],
    },
    'annealing gs': {
        'b': [5700100, 5710100, 5735800],
        'c': [5373493, 5461276, 5391196],
        'e': [4312187, 4355104, 4467101],
        'f': [5301656, 5242866, 5259489],
    },
}

def extract_data(data, key):
    return [np.mean(val) for val in data[key].values()]

score_hist = axs[0]

w = 0.2
labels = ['B', 'C', 'E', 'F']
x = np.arange(len(labels))

score_hist.bar(x - 1.5 * w, extract_data(scores, 'hillclimb'), w, label='hillclimb', alpha=.75)
score_hist.bar(x - 0.5 * w, extract_data(scores, 'annealing rs'), w, label='annealing rs', alpha=.75)
score_hist.bar(x + 0.5 * w, extract_data(scores, 'annealing gs'), w, label='annealing gs', alpha=.75)
score_hist.bar(x + 1.5 * w, extract_data(scores, 'genetic'), w, label='genetic', alpha=.75)

score_hist.set_ylabel('Scores')
score_hist.set_title('Score by Dataset')
score_hist.set_xticks(x)
score_hist.set_xticklabels(labels)
score_hist.legend(bbox_to_anchor=(1, 0), loc="lower left")

time_hist = axs[1]

time_hist.bar(x - 1.5 * w, extract_data(times, 'hillclimb'), w, label='hillclimb', alpha=.75)
time_hist.bar(x - 0.5 * w, extract_data(times, 'annealing gs'), w, label='annealing gs', alpha=.75)
time_hist.bar(x + 0.5 * w, extract_data(times, 'annealing rs'), w, label='annealing rs', alpha=.75)
time_hist.bar(x + 1.5 * w, extract_data(times, 'genetic'), w, label='genetic', alpha=.75)

# Plot known times that are WAY too large
time_hist.text(1 - 1.5 * w, 150 / 1.25, "{:.0f}".format(np.mean(times['hillclimb']['c'])), ha='center', va='center')
time_hist.text(1 + 1.5 * w, 150 / 1.25, "{:.0f}".format(np.mean(times['genetic']['c'])), ha='center', va='center')

time_hist.set_ylabel('Time (s)')
time_hist.set_title('Execution time by Dataset')
time_hist.set_xticks(x)
time_hist.set_xticklabels(labels)

time_hist.set_ylim(top=150)

fig.tight_layout()

fig.savefig('dataset_score.png')
plt.show()

