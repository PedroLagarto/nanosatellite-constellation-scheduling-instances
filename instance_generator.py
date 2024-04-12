import numpy as np

class InstanceGenerator:
    #crete init with data hints
    def __init__(self, S: int, J: int, T: int, num_const_tasks: int):
        self.S = S
        self.J = J
        self.T = T
        self.num_const_tasks = num_const_tasks
        self.initialize_instance()
        
    def initialize_instance(self):
        
        self.power_resource = np.zeros((self.S, self.T))
        self.power_usage = np.zeros((self.S, self.J))
        self.priority = np.zeros((self.S, self.J))
        self.min_startup = np.zeros((self.S, self.J))
        self.max_startup = np.zeros((self.S, self.J))
        self.min_cpu_time = np.zeros((self.S, self.J))
        self.max_cpu_time = np.zeros((self.S, self.J))
        self.min_period_job = np.zeros((self.S, self.J))
        self.max_period_job = np.zeros((self.S, self.J))
        self.win_min = np.zeros((self.S, self.J))
        self.win_max = np.zeros((self.S, self.J))
        self.max_startup_constellation = np.zeros(self.J)
        self.min_startup_constellation = np.zeros(self.J)
        self.constellation_tasks = np.zeros(self.J)
        self.constellation_tasks[:self.num_const_tasks] = 1


    def generate_instance(self):
        for s in range(self.S):
            orbit_power = np.loadtxt('irradiation/resource.csv')
            orbit_start = np.random.randint(0, 600)
            self.priority[s] = np.arange(self.J) + 1
            np.random.shuffle(self.priority[s])
            for j in range(self.J):
                self.power_resource[s] = orbit_power[orbit_start:orbit_start+self.T]
                min_power = 0.01
                max_power = 1.00
                self.power_usage[s][j] = np.random.rand()
                self.power_usage[s][j] = (max_power - min_power) * self.power_usage[s][j] + min_power

                self.min_cpu_time[s][j] = np.random.randint(1, self.T / 10)
                self.max_cpu_time[s][j] = np.random.rand()
                self.max_cpu_time[s][j] = self.max_cpu_time[s][j] * (self.T / 2 - self.min_cpu_time[s][j]) + self.min_cpu_time[s][j]
                self.max_cpu_time[s][j] = self.max_cpu_time[s][j].astype(int)

                min_limit = 1
                max_limit_min_startup = max(1, int(self.T / 30))
                max_limit_max_startup = max(max_limit_min_startup + 1, int(self.T / 15))

                # Ensure min_startup is between 1 and T/30
                self.min_startup[s][j] = np.random.randint(min_limit, max_limit_min_startup + 1)
                
                # Ensure max_startup is between T/30 and T/15
                self.max_startup[s][j] = np.random.randint(max_limit_min_startup, max_limit_max_startup + 1)

                # max_possible_startup = (self.T / self.min_cpu_time[s][j]).astype(int)
                # self.min_startup[s][j] = np.random.rand() * (max_possible_startup - 1) + 1
                # self.min_startup[s][j] = self.min_startup[s][j].astype(int)
                # self.max_startup[s][j] = np.random.rand()
                # self.max_startup[s][j] = self.max_startup[s][j] * (self.T - self.min_startup[s][j]) + self.min_startup[s][j]
                # self.max_startup[s][j] = self.max_startup[s][j].astype(int)

                # max_possible_job_period = (self.T / self.min_startup[s][j]).astype(int)
                # self.min_period_job[s][j] = np.random.rand()
                # self.min_period_job[s][j] = self.min_period_job[s][j] * (max_possible_job_period - 1) + 1
                # self.min_period_job[s][j] = self.min_period_job[s][j].astype(int)

                # self.max_period_job[s][j] = np.random.rand()
                # self.max_period_job[s][j] = self.max_period_job[s][j] * (self.T - self.min_period_job[s][j]) + self.min_period_job[s][j]
                # self.max_period_job[s][j] = self.max_period_job[s][j].astype(int)

                self.min_period_job[s][j] = np.random.randint(10, 21)
                self.max_period_job[s][j] = np.random.randint(40, self.T + 1)

                self.win_min[s][j] = np.random.randint(0, int(self.T/6) + 1)
                self.win_max[s][j] = np.random.randint(int(self.T*5/6), self.T + 1)
                self.win_min[s][j] = self.win_min[s][j].astype(int)
                self.win_max[s][j] = self.win_max[s][j].astype(int)

        for j in range(self.J):
            if self.constellation_tasks[j] == 1:
                # max_possible_startup = (self.T / self.min_cpu_time[s][j]).astype(int)
                # self.min_startup_constellation[j] = np.random.rand() * (max_possible_startup - 1) + 1
                # self.min_startup_constellation[j] = self.min_startup[s][j].astype(int)
    
                # self.max_startup_constellation[j] = np.random.rand()
                # self.max_startup_constellation[j] = self.max_startup[s][j] * (self.T - self.min_startup[s][j]) + self.min_startup[s][j]
                # self.max_startup_constellation[j] = self.max_startup[s][j].astype(int)
                self.min_startup_constellation[j] = np.random.randint(1, 3)
                self.max_startup_constellation[j] = np.random.rand()
                self.max_startup_constellation[j] = self.max_startup[s][j] * (self.T - self.min_startup[s][j]) + self.min_startup[s][j]
                self.max_startup_constellation[j] = self.max_startup[s][j].astype(int)

        return {
            "number_satellites": self.S,
            "number_jobs": self.J,
            "T": self.T,
            "power_use": self.power_usage.tolist(),
            "power_resource": self.power_resource.tolist(),
            "min_cpu_time": self.min_cpu_time.astype(int).tolist(),
            "max_cpu_time": self.max_cpu_time.astype(int).tolist(),
            "min_period_job": self.min_period_job.astype(int).tolist(),
            "max_period_job": self.max_period_job.astype(int).tolist(),
            "min_startup": self.min_startup.astype(int).tolist(),
            "max_startup": self.max_startup.astype(int).tolist(),
            "priority": self.priority.tolist(),
            "win_min": self.win_min.astype(int).tolist(),
            "win_max": self.win_max.astype(int).tolist(),
            "constellation_tasks": self.constellation_tasks.tolist(),
            "max_statup_constellation": self.max_startup_constellation.astype(int).tolist(),
            "min_statup_constellation": self.min_startup_constellation.astype(int).tolist()
        }   