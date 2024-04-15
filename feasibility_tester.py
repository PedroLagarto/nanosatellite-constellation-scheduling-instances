import os
from instance_generator import InstanceGenerator
from problem import Problem
from gurobipy import GRB

class FeasibilityTester:
    def __init__(self, S=5, J=10, T=150, num_const_tasks=5):
        self.S = S
        self.J = J
        self.T = T
        self.const_tasks = num_const_tasks
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
                self.save_python_file(instance)
                break  # Exit the loop if a feasible instance is found
            else:
                self.problem.model.computeIIS()
                self.problem.model.write("model.ilp")
            print("Counter:", counter)
            counter += 1  # Increment the counter
        print("Timeout reached. No feasible instance found.")

    def save_python_file(self, instance):
        filename = f"{self.S}_{self.J}_{self.T}_{self.const_tasks}"
        with open(filename, 'w') as file:
            for key, value in instance.items():
                # Create a list representation of the value which is assumed to be a list
                list_content = ', '.join(repr(v) for v in value)
                # Write a line defining a list with the key as the name and the list content as the elements
                file.write(f"{key} = [{list_content}]\n")

if __name__ == '__main__':
    tester = FeasibilityTester()
    tester.build_and_solve_problem()
    print("Feasible instance:")