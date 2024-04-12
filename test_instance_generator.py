import unittest
from instance_generator import InstanceGenerator

class TestInstanceGenerator(unittest.TestCase):
    def test_initialize_instance(self):
        generator = InstanceGenerator(5, 10, 100, 3)
        generator.initialize_instance()

        self.assertEqual(generator.power_resource.shape, (5, 100))
        self.assertEqual(generator.power_usage.shape, (5, 10))
        self.assertEqual(generator.priority.shape, (5, 10))
        self.assertEqual(generator.min_startup.shape, (5, 10))
        self.assertEqual(generator.max_startup.shape, (5, 10))
        self.assertEqual(generator.min_cpu_time.shape, (5, 10))
        self.assertEqual(generator.max_cpu_time.shape, (5, 10))
        self.assertEqual(generator.min_period_job.shape, (5, 10))
        self.assertEqual(generator.max_period_job.shape, (5, 10))
        self.assertEqual(generator.win_min.shape, (5, 10))
        self.assertEqual(generator.win_max.shape, (5, 10))
        self.assertEqual(generator.max_startup_constellation.shape, (10,))
        self.assertEqual(generator.min_startup_constellation.shape, (10,))
        self.assertEqual(generator.constellation_tasks.shape, (10,))

    def test_generate_instance(self):
        generator = InstanceGenerator(5, 10, 100, 3)
        instance = generator.generate_instance()

        self.assertEqual(instance["number_satellites"], 5)
        self.assertEqual(instance["number_jobs"], 10)
        self.assertEqual(instance["T"], 100)
        self.assertEqual(len(instance["power_use"]), 5)
        self.assertEqual(len(instance["power_use"][0]), 10)
        self.assertEqual(len(instance["power_resource"]), 5)
        self.assertEqual(len(instance["power_resource"][0]), 100)
        self.assertEqual(len(instance["min_cpu_time"]), 5)
        self.assertEqual(len(instance["min_cpu_time"][0]), 10)
        self.assertEqual(len(instance["max_cpu_time"]), 5)
        self.assertEqual(len(instance["max_cpu_time"][0]), 10)
        self.assertEqual(len(instance["min_job_period"]), 5)
        self.assertEqual(len(instance["min_job_period"][0]), 10)
        self.assertEqual(len(instance["max_job_period"]), 5)
        self.assertEqual(len(instance["max_job_period"][0]), 10)
        self.assertEqual(len(instance["min_startup"]), 5)
        self.assertEqual(len(instance["min_startup"][0]), 10)
        self.assertEqual(len(instance["max_startup"]), 5)
        self.assertEqual(len(instance["max_startup"][0]), 10)
        self.assertEqual(len(instance["priority"]), 5)
        self.assertEqual(len(instance["priority"][0]), 10)
        self.assertEqual(len(instance["win_min"]), 5)
        self.assertEqual(len(instance["win_min"][0]), 10)
        self.assertEqual(len(instance["win_max"]), 5)
        self.assertEqual(len(instance["win_max"][0]), 10)
        self.assertEqual(len(instance["constelation_tasks"]), 10)
        self.assertEqual(len(instance["max_statup_constellation"]), 10)
        self.assertEqual(len(instance["min_statup_constellation"]), 10)

if __name__ == '__main__':
    unittest.main()