from problem import Problem, TestFiles

testfile = TestFiles.test_f

p = Problem.from_file(testfile)
p.hillclimbing()
print(p.total_score)
# p.visualize(testfile)

