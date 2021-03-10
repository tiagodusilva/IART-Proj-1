from problem import Problem, TestFiles

p = Problem.from_file(TestFiles.test_a)
p.insert_test_sol()
p.visualize()

