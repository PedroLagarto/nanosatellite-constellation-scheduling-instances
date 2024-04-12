import os
from instance_generator import InstanceGenerator
from problem import Problem
from gurobipy import GRB

class FeasibilityTester:
    def __init__(self, S=10, J=10, T=120, num_const_tasks=5):
        self.instance_generator = InstanceGenerator(S, J, T, num_const_tasks)
        self.problem = Problem()

    def generate_instance(self):
        instance = self.instance_generator.generate_instance()
        return instance

    def build_and_solve_problem(self):
        max_iter = 60  # Set the timeout value in seconds
        counter = 0  # Initialize the counter
        while counter < max_iter:
            instance = self.generate_instance()
            self.problem.set_instance(instance)
            self.problem.build_and_solve()
            if self.problem.model.status != GRB.Status.INFEASIBLE:
                print("Feasible instance found!")
                break  # Exit the loop if a feasible instance is found
            print("Counter:", counter)
            counter += 1  # Increment the counter
        print("Timeout reached. No feasible instance found.")

if __name__ == '__main__':
    tester = FeasibilityTester()
    tester.build_and_solve_problem()
    print("Feasible instance:")