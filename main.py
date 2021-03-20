from problem import Problem, TestFiles

testfile = TestFiles.test_e

p = Problem.from_file(testfile)
p.hillclimbing_fast()
print(f"Final Score: {p.total_score}")
# p.annealing()
p.tabu_search()
p.dump_solution(testfile.replace("test/", "sol/"))
