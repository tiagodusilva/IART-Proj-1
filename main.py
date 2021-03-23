import sys
from problem import Problem, TestFiles

testfile = TestFiles.test_f

print(f"DATASET: {testfile}")

p = Problem.from_file(testfile)
p.hillclimbing(reavaluations=20)

print(f"Hill Climbing Score: {p.total_score}")

p.annealing()
# p.tabu_search()

print(f"Final Score: {p.total_score}")

p.dump_solution(testfile.replace("test/", "sol/"))

if len(sys.argv) > 1 and sys.argv[1].lower() == '-v':
    from visualizer import plot_result
    import matplotlib.pyplot as plt

    fig, ax = plot_result(p, testfile, show=True)
    # fig.savefig("uwu.png", dpi=200)
