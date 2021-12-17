# A branch-and-price algorithm for nanosatellite task scheduling to improve mission quality-of-service
 This repository is comprised of all instances used for computational benchmarks in the paper entitled "A branch-and-price algorithm for nanosatellite task scheduling to improve mission quality-of-service" submitted to the European Journal of Operational Research.

# Abstract 
Satellite scheduling is concerned with the assignment of start and finish times for tasks while considering the mission objective, available resources, and constraints. This scheduling problem is especially critical in nanosatellites, given that resources are more scarce than in traditionally-sized spacecrafts. Despite having its own set of constraints and being increasingly deployed, nanosatellite task scheduling has received little attention in the literature. In this paper, we advance the state-of-the-art by devising an effective solution approach for a nanosatellite task scheduling problem. We resort to the Dantzig-Wolfe decomposition to explore the special structure of an existing mixed-integer linear programming (MILP) formulation, decomposing it by tasks, which results in a novel profile-based formulation for the problem. To solve the resulting formulation, we propose a branch-and-price (B\&P) algorithm that is suitable for the scheduling of a large number of tasks over an expanded time horizon. Furthermore, we design a dynamic programming algorithm for generating feasible schedules instead of solving the pricing subproblem with an MILP solver, among other algorithmic strategies. Computational experiments using instances that represent realistic scenarios showed that the B\&P algorithm is considerably more efficient in solving large instances when compared to commercial solvers. Overall, the proposed solution strategy empowers the decision maker to plan more complex missions, in an optimal or nearly-optimal manner and within a reasonable computation time.
