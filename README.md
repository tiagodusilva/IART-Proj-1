# IART-Proj-1

## Instructions

### Required Software

- Python 3.7 or above
- Numpy and MatPlotLib modules ~ If you wish to plot the solution (`--plot`)

or

- PyPy3 ~ For faster execution, cannot render plots

### Execution

You can run using either `python main.py` or `pypy3 main.py` followed by the required arguments. Use `-h` to show the parameters that are also shown below:

```
usage: main.py [-h] [-v] [-t {a,b,c,d,e,f}] [-s SEED] [-p] [-d] [--hill] [-sa]
               [-sat ANNEALING_TEMPERATURE] [-saic ANNEALING_INITIAL_COOLING]
               [-safc ANNEALING_FINAL_COOLING] [-g] [-gg GEN_GENERATIONS]
               [-gp GEN_POPULATION] [-gm GEN_MUTATION_CHANCE] [-g1pc] [-g2pc]
               [-rs] [-os] [-gs]
```
```
Book Scanning ~ IART Proj 1 g42

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase verbosity
  -t {a,b,c,d,e,f}, --test {a,b,c,d,e,f}
                        Test file to use
  -s SEED, --seed SEED  Seed for the random generator
  -p, --plot, --plotting
                        Plot result, incompatible with PyPy
  -d, --dump            Dumps the solution into the 'sol' directory
  --hill, --hillclimbing
                        Use hill climbing
  -sa, --annealing      Use simulated annealing
  -sat ANNEALING_TEMPERATURE, --annealing-temperature ANNEALING_TEMPERATURE
                        Simulated annealing initial temperature
  -saic ANNEALING_INITIAL_COOLING, --annealing-initial-cooling ANNEALING_INITIAL_COOLING
                        Simulated initial annealing cooling
  -safc ANNEALING_FINAL_COOLING, --annealing-final-cooling ANNEALING_FINAL_COOLING
                        Simulated final annealing cooling
  -g, --genetic, --gen  Use genetic algorithm
  -gg GEN_GENERATIONS, --gen-generations GEN_GENERATIONS
                        Genetic algorithm ~ Number of generations
  -gp GEN_POPULATION, --gen-population GEN_POPULATION
                        Genetic algorithm ~ Population size
  -gm GEN_MUTATION_CHANCE, --gen-mutation-chance GEN_MUTATION_CHANCE
                        Genetic algorithm ~ Mutation chance
  -g1pc, --gen-one-point-crossover
                        Genetic algorithm ~ One point crossover operator
  -g2pc, --gen-two-point-crossover
                        Genetic algorithm ~ Two point crossover operator (OX1)
  -rs, --random-start   Sets the inital solution to random
  -os, --ordered-start  Sets the inital solution to books ordered by score
  -gs, --greedy-start   Sets the inital solution to greedy search
```


## Checkpoints

### Checkpoint 1
The presentation can be found in [Google Slides](https://docs.google.com/presentation/d/1boKHYrRc8i1GjkOR6qIlVy_0Im2Yd7wn0_Prbc8IgLc/edit?usp=sharing). A pdf copy is also present in [the repository](docs/checkpoint1.pdf).

### Final Delivery
The presentation can be found in [Google Slides](https://docs.google.com/presentation/d/1XJ32qSG7nPp5iMJkZF4JA-mPBLOyOiUC-clOXN1LV8w/edit?usp=sharing). A pdf copy is also present in [the repository](docs/final_delivery.pdf).
