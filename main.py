from problem import Problem, TestFiles
# from visualizer import plot_result

testfile = TestFiles.test_d

print(f"DATASET: {testfile}")

p = Problem.from_file(testfile)
p.hillclimbing(reavaluations=20)

print(f"Final Score: {p.total_score}")

# p.annealing()
# p.tabu_search()

p.dump_solution(testfile.replace("test/", "sol/"))

# fig, ax = plot_result(p, testfile)
# fig.savefig("uwu.png", dpi=200)

