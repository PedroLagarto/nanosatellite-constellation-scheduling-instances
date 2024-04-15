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
        # Parameters
        min_power = 0.3
        max_power = 2.50

        for s in range(self.S):
            # Random start for each satellite
            orbit_power = np.loadtxt('irradiation/resource.csv')
            orbit_start = np.random.randint(0, 600)

            # Random priority for each satellite
            self.priority[s] = np.arange(self.J) + 1
            np.random.shuffle(self.priority[s])

            for j in range(self.J):
                # Uniform distribution of power usage between [min_power, max_power]
                self.power_resource[s] = orbit_power[orbit_start:orbit_start+self.T]
                self.power_usage[s][j] = np.random.rand()
                self.power_usage[s][j] = (max_power - min_power) * self.power_usage[s][j] + min_power

                # Random startup time between [1, T/45]
                min_limit = 1
                max_limit_min_startup = max(1, np.ceil(self.T / 45))
                self.min_startup[s][j] = np.random.randint(min_limit, max_limit_min_startup)

                # Random startup time between [min_startup, T/45]
                max_limit_max_startup = max(max_limit_min_startup + 1, np.ceil(self.T / 15))
                self.max_startup[s][j] = np.random.randint(max_limit_min_startup + 1, max_limit_max_startup)

                # Random min
                self.min_cpu_time[s][j] = np.random.randint(1, np.ceil(self.T / 10))
                self.max_cpu_time[s][j] = int(np.random.rand() * (np.ceil(self.T / 4) - self.min_cpu_time[s][j]) + self.min_cpu_time[s][j])

                # Random min period between [min_cpu_time, T/4] and max period between [min_period, T]
                self.min_period_job[s][j] = np.random.uniform(self.min_cpu_time[s][j], np.ceil(self.T / 4))
                self.max_period_job[s][j] = np.random.uniform(self.min_period_job[s][j], self.T)
                

                self.win_min[s][j] = np.random.randint(0, np.ceil(self.T/5))
                self.win_max[s][j] = np.random.randint(self.T - np.ceil(self.T/5), self.T)

        for j in range(self.J):
            if self.constellation_tasks[j] == 1:
                self.min_startup_constellation[j] = np.random.randint(1, 3)
                self.max_startup_constellation[j] = np.random.rand()
                self.max_startup_constellation[j] = self.max_startup[s][j] * (self.T - self.min_startup[s][j]) + self.min_startup[s][j]
                self.max_startup_constellation[j] = self.max_startup[s][j].astype(int)
                self.max_startup_constellation[j] = np.random.randint(3*self.S, 6*self.S)

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