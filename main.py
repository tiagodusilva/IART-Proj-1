from problem import Problem, TestFiles

testfile = TestFiles.test_c

p = Problem.from_file(testfile)
p.hillclimbing(reavaluations=4)
print(f"{testfile}")
print(f"Final Score: {p.total_score}")
# p.annealing()
# p.tabu_search()
p.dump_solution(testfile.replace("test/", "sol/"))
