import simpy
import random

class QueueSystem:
    def __init__(self, env, num_servers, arrival_rate, service_rate):
        self.env = env
        self.servers = simpy.Resource(env, num_servers)
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.total_wait_time = 0
        self.total_customers = 0
        self.server_busy_time = 0
        self.customer_log = []  # Stores arrival & service times

    def customer_process(self):
        customer_id = 1
        while True:
            yield self.env.timeout(random.expovariate(self.arrival_rate))  # Time until next customer arrives
            self.env.process(self.serve_customer(customer_id))
            customer_id += 1

    def serve_customer(self, customer_id):
        arrival_time = self.env.now
        with self.servers.request() as request:
            yield request  # Wait for a free server
            wait_time = self.env.now - arrival_time  # Calculate wait time
            self.total_wait_time += wait_time
            self.total_customers += 1

            service_time = random.expovariate(self.service_rate)  # Generate service time
            self.server_busy_time += service_time
            service_start_time = self.env.now
            yield self.env.timeout(service_time)  # Serve the customer
            service_end_time = self.env.now

            # Store customer log (arrival, service start, service end)
            self.customer_log.append((customer_id, arrival_time, service_start_time, service_end_time))

# Get user input
arrival_rate = float(input("Enter the customer arrival rate (λ): "))
service_rate = float(input("Enter the service rate per server (μ): "))
num_servers = int(input("Enter the number of servers (c): "))

# Set up simulation
env = simpy.Environment()
queue_system = QueueSystem(env, num_servers, arrival_rate, service_rate)
env.process(queue_system.customer_process())

# Run simulation for 100 time units
env.run(until=100)

# Calculate statistics
average_wait_time = queue_system.total_wait_time / queue_system.total_customers if queue_system.total_customers else 0
server_utilization = (queue_system.server_busy_time / (num_servers * 100)) * 100  # As percentage

# Display customer log
print("\nCustomer Log:")
print(f"{'ID':<5} {'Arrived':<10} {'Service Start':<15} {'Service End'}")
for customer in queue_system.customer_log:
    print(f"{customer[0]:<5} {customer[1]:<10.2f} {customer[2]:<15.2f} {customer[3]:.2f}")

# Display final results
print("\nSimulation Results:")
print(f"Total customers served: {queue_system.total_customers}")
print(f"Average waiting time: {average_wait_time:.2f} time units")
print(f"Server utilization: {server_utilization:.2f}%")
