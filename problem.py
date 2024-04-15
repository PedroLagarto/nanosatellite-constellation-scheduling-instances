import gurobipy as gp
from gurobipy import GRB

class Problem:
    """
    Defines a problem instance.

    Parameters:
    - instance (dict): Generated by higher level functions, constains the instance data.
    """
    def __init__(self, instance = None):
        self.instance = instance
        self.model = gp.Model("Problem")
        self.define_solver_parameters()
    
    def set_instance(self, instance):
        self.instance = instance
    
    def unpack_instance(self):

        self.recurso = self.instance['power_resource']
        self.J = self.instance['number_jobs'] # número de tarefas
        self.T = self.instance['T'] # número de unidades de tempo
        self.S = self.instance['number_satellites'] # número de satelites
        self.constelation_tasks = self.instance['constellation_tasks'] # representa as tarefas de constelação
        self.priority = self.instance['priority'] # prioridade de cada tarefa
        self.uso_p = self.instance['power_use'] # recurso utilizado por cada tarefa
        self.min_statup = self.instance['min_startup'] # tempo mínimo de vezes que uma tarefa pode iniciar
        self.max_statup = self.instance['max_startup'] # tempo máximo de vezes que uma tarefa pode iniciar
        self.min_cpu_time = self.instance['min_cpu_time'] # tempo mínimo de unidades de tempo que uma tarefa pode consumir em sequência
        self.max_cpu_time = self.instance['max_cpu_time'] # tempo máximo de unidades de tempo que uma tarefa pode consumir em sequência
        self.min_periodo_job = self.instance['min_period_job'] # tempo mínimo que uma tarefa deve esperar para se repetir
        self.max_periodo_job = self.instance['max_period_job'] # tempo máximo que uma tarefa pode esperar para se repetir
        self.win_min = self.instance['win_min']
        self.win_max = self.instance['win_max']
        self.max_startup_constellation = self.instance['max_statup_constellation']
        self.min_startup_constellation = self.instance['min_statup_constellation']
        self.soc_inicial = 0.7
        self.limite_inferior = 0.0
        self.ef = 0.9
        self.v_bat = 3.6
        self.q = 5
        self.bat_usage = 5


    def build_and_solve(self):
        self.unpack_instance()
        self.build_model()
        self.model.optimize()

    def build_model(self):
        """
        Builds the Gurobi model for the instance.

        """
        self.build_variables()
        self.set_objective()
        self.add_constraints()
    
    def define_solver_parameters(self):
        self.model.setParam('MIPFocus', 1)
        self.model.setParam('TimeLimit', 300000)
        self.model.setParam('PoolSolutions', 1)  # Keep only the first solution found
        self.model.setParam('PoolSearchMode', 1)  # Stop as soon as a feasible solution is found
        self.model.setParam('OutputFlag', 1)  # Disable output (stdout

    def build_variables(self):
        self.x = {}
        self.phi = {}
        self.alpha = {}
        self.soc = {}
        self.i = {}
        self.b = {}
        for s in range(self.S):
            for j in range(self.J):  # Add range() function to iterate over self.J
                for t in range(self.T):
                    self.x[s,j,t] = self.model.addVar(name="x(%s,%s,%s)" % (s, j, t), lb=0, ub=1, vtype="BINARY")
                for t in range(self.T):
                    self.phi[s,j,t] = self.model.addVar(name="phi(%s,%s,%s)" % (s, j, t), lb=0, ub=1, vtype="BINARY")
        for s in range(self.S):
            for t in range(self.T):
                self.alpha[s,t] = self.model.addVar(lb=0,vtype=GRB.CONTINUOUS, name="alpha(%s,%s)" % (s, t))
                self.soc[s, t] = self.model.addVar(vtype=GRB.CONTINUOUS, name="soc(%s,%s)" % (s, t))
                self.i[s, t] = self.model.addVar(
                    lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="i(%s,%s)" % (s, t)
                )
                self.b[s, t] = self.model.addVar(
                    lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="b(%s,%s)" % (s, t)
                )

    def set_objective(self):
        self.model.setObjective(0)  # Setting a constant objective
    
    def add_constraints(self):
        self.add_power_constraints()
        self.add_phi_constraints()
        self.add_job_constraints()

    def add_power_constraints(self):
        for s in range(self.S):
            for t in range(self.T):
                self.model.addConstr(
                    gp.quicksum(self.uso_p[s][j] * self.x[s, j, t] for j in range(self.J))
                    <= self.recurso[s][t] + self.bat_usage * self.v_bat*(1 - self.alpha[s,t])
                )
    
            for t in range(self.T):
                self.model.addConstr(
                    (
                        gp.quicksum(self.uso_p[s][j] * self.x[s, j, t] for j in range(self.J)) + self.b[s,t]
                        == self.recurso[s][t]
                    )
                )
            for t in range(self.T):
                self.model.addConstr(self.b[s, t] / self.v_bat >= self.i[s, t])
                if t == 0:
                    self.model.addConstr(self.soc[s, t] == self.soc_inicial + (self.ef / self.q) * (self.i[s, t] / 60))
                else:
                    self.model.addConstr(self.soc[s, t] == self.soc[s, t - 1] + (self.ef / self.q) * (self.i[s, t] / 60))
                self.model.addConstr(self.limite_inferior <= self.soc[s, t])
                self.model.addConstr(self.soc[s, t] <= 1)

    def add_phi_constraints(self):
        for s in range(self.S):
            for t in range(self.T):
                for j in range(self.J):
                    if t == 0:
                        self.model.addConstr(self.phi[s, j, t] >= self.x[s, j, t] - 0)
                    else:
                        self.model.addConstr(self.phi[s, j, t] >= self.x[s, j, t] - self.x[s, j, t - 1])

                    self.model.addConstr(self.phi[s, j, t] <= self.x[s, j, t])

                    if t == 0:
                        self.model.addConstr(self.phi[s, j, t] <= 2 - self.x[s, j, t] - 0)
                    else:
                        self.model.addConstr(self.phi[s, j, t] <= 2 - self.x[s, j, t] - self.x[s, j, t - 1])
    
    def add_job_constraints(self):
        #Constellation Constraints
        for j in range(self.J):
            if self.constelation_tasks[j] == 1:
                self.model.addConstr(
                    gp.quicksum(self.phi[s, j, t] for s in range(self.S) for t in range(self.T)) <= self.max_startup_constellation[j]
                    , name = f"global_startup_max_{j}"
                )
                self.model.addConstr(
                    gp.quicksum(self.phi[s, j, t] for s in range(self.S) for t in range(self.T)) >= self.min_startup_constellation[j]
                    , name = f"global_startup_min_{j}"
                )   
        for s in range(self.S):
            for j in range(self.J):
                self.model.addConstr(gp.quicksum(self.phi[s, j, t] for t in range(self.T)) >= self.min_statup[s][j], name = f"local_min_startup_{s,j}")
                self.model.addConstr(gp.quicksum(self.phi[s, j, t] for t in range(self.T)) <= self.max_statup[s][j], name = f"local_startup_max_{s,j}")

                self.model.addConstr(gp.quicksum(self.x[s, j, t] for t in range(self.win_min[s][j]+1)) == 0)
                self.model.addConstr(gp.quicksum(self.x[s, j, t] for t in range(self.win_max[s][j]+1, self.T)) == 0)

            for j in range(self.J):
                for t in range(0, self.T - self.min_periodo_job[s][j] + 1):
                    self.model.addConstr(
                        gp.quicksum(self.phi[s, j, t_] for t_ in range(t, t + self.min_periodo_job[s][j]))
                        <= 1,
                        name = f"min_periodo_job_{s,j,t}"
                    )
                for t in range(0, self.T - self.max_periodo_job[s][j] + 1):
                    self.model.addConstr(
                        gp.quicksum(self.phi[s, j, t_] for t_ in range(t, t + self.max_periodo_job[s][j]))
                        >= 1,
                        name = f"max_periodo_job_{s,j,t}"
                    )
                for t in range(0, self.T - self.min_cpu_time[s][j] + 1):
                    self.model.addConstr(
                        gp.quicksum(self.x[s, j, t_] for t_ in range(t, t + self.min_cpu_time[s][j]))
                        >= self.min_cpu_time[s][j] * self.phi[s, j, t]
                    )
                for t in range(0, self.T - self.max_cpu_time[s][j]):
                    self.model.addConstr(
                        gp.quicksum(self.x[s, j, t_] for t_ in range(t, t + self.max_cpu_time[s][j] + 1))
                        <= self.max_cpu_time[s][j]
                    )
                for t in range(self.T - self.min_cpu_time[s][j] + 1, self.T):
                    self.model.addConstr(
                        gp.quicksum(self.x[s, j, t_] for t_ in range(t, self.T)) >= (self.T - t) * self.phi[s, j, t]
                    )
                for t in range(self.T):
                        self.model.addConstr(gp.quicksum(self.phi[s,j,t] for t in range(t,min(self.T, t+self.min_cpu_time[s][j]+1))) <= 1, name = f"VI_min_CPU_TIME_phi({j},{t})")
                        self.model.addConstr(gp.quicksum(self.x[s,j,t] for t in range(self.T)) <= self.max_cpu_time[s][j]*gp.quicksum(self.phi[s,j,t] for t in range(self.T)),name = f"VI_max_cpu_time_2({j})")

                for t in range(self.T - self.max_cpu_time[s][j]):
                        self.model.addConstr(gp.quicksum(self.x[s,j,t] for t in range(t, t + self.max_cpu_time[s][j])) <= self.max_cpu_time[s][j]*gp.quicksum(self.phi[s,j,t] for t in range(max(t - self.max_cpu_time[s][j] + 1,0),t + self.max_cpu_time[s][j], 1)), name = f"VI_max_cpu_time_3({j},{t})")

                for t in range(self.T - self.min_periodo_job[s][j]+1):
                        self.model.addConstr(gp.quicksum(self.x[s,j,t] for t in range(t, t + self.min_periodo_job[s][j])) <= self.min_periodo_job[s][j], name = f"VI_min_period_btw_jobs_2({j},{t})")

                if self.max_cpu_time[s][j] < self.max_periodo_job[s][j] - self.min_cpu_time[s][j]:
                        for t in range(self.T - self.max_cpu_time[s][j]):
                                self.model.addConstr(self.phi[s,j,t] + self.x[s,j,t+self.max_cpu_time[s][j]]<=1)


