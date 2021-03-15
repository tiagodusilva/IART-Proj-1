from problem import Problem, TestFiles

testfile = TestFiles.test_b

p = Problem.from_file(testfile)
p.hillclimbing()
print(p.total_score)
p.visualize(testfile)
# p.dump_solution(testfile.replace("test/", "sol/"))

