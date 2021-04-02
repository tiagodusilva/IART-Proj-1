import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn')

fig = plt.figure()
ax = fig.subplots()

scores = {
    'single point': {
        0: [5458300, 5423100, 5377900, 5395900, 5245600],
        0.05: [5225000, 5425300, 5410400, 5346600, 5393800],
        0.1: [5229100, 5232700, 5370000, 5427700, 5385000, 5356300, 5225300, 5429700, 5404200, 5336700],
        0.15: [5348300, 5393500, 5448700, 5341900, 5326500, 5275900, 5388300, 5185800, 5385700, 5274200],
        0.2: [5375200, 5275700, 5354300, 5357100, 5301100],
    },
    'ox1': {
        0: [5108100, 5207900, 5097500, 5197700, 5125000],
        0.05: [5169800, 5194100, 5182300, 5153400, 5003000],
        0.1: [5267500, 5293400, 5206400, 5178100, 5183700, 5167200, 5034500, 5058700, 5100100, 5196200, 5055100, 5105700],
        0.15: [5084900, 5065900, 5217100, 5147800, 5244300, 5262300, 5166400, 5254000],
        0.2: [4990600, 5160000, 5074200, 5188900, 5133700],
    },
}

def extract_data(data, key):
    return [np.mean(val) for val in data[key].values()]

def to_percent(it):
    return [v * 100 for v in it]

ax.plot(to_percent(scores['single point'].keys()), extract_data(scores, 'single point'), marker='.', label='Single Point Crossover')
ax.plot(to_percent(scores['ox1'].keys()), extract_data(scores, 'ox1'), marker='.', label='OX1')

ax.set_xlabel('Mutation Chance (%)')
ax.set_ylabel('Score')

ax.set_title('Genetic Algorithm ~ Score by Mutation Chance')

ax.legend()

fig.tight_layout()

fig.savefig('genetic_stats.png')
plt.show()

