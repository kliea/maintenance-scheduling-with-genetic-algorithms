import numpy as np

# Define the problem parameters
num_units = 7
num_intervals = 4
max_loads = [80, 90, 65, 70]
totalcap = 0  # Initialize totalcap

# Define the unit data for its capacities and maintenance intervals
unitData = np.array([
    (20, 2),
    (15, 2),
    (35, 1),
    (40, 1),
    (15, 1),
    (15, 1),
    (10, 1)
])

#generate a chromosome
def generateGenome(unitData, num_intervals, max_loads, totalcap):
    #generate empty chromosome
    chromosome = np.zeros((num_units, num_intervals), dtype=int)
    
      
    for unit in range(num_units):
        if unitData[unit][1] > num_intervals:
            raise ValueError("Unit's required interval must not be greater than load interval")

        # maintenance of any unit starts at the beginning of an interval and finishes at the same or adjacent interval. example required interval for unit = 2 then [0 0 1 1] [1 1 0 0 ] [0 1 1 0]    
        startInterval = np.random.randint(0, num_intervals - unitData[unit][1] + 1)

        for interval in range(startInterval, startInterval + unitData[unit][1]):
            chromosome[unit, interval] = 1    
        
        #define total capacity
        totalcap = totalcap + unitData[unit][0]   
    
    return chromosome, totalcap

#generate chromosome
chromosome, totalcap = generateGenome(unitData, num_intervals, max_loads, totalcap)

#calculate fitness of the chromosome
def fitness(chromosome, unitData, max_loads, totalcap):
    # Reshape unitData[:,0] to match the shape of chromosome
    unit_capacity = unitData[:,0].reshape(-1, 1)
    
    # Calculate the total capacity for each interval
    installed_capacity = np.sum(chromosome * unit_capacity, axis=0)
    print(installed_capacity)
    
    # Calculate the difference between the total capacity and the maximum loads
    total_installed_capacity = np.abs(totalcap - installed_capacity)
    print(total_installed_capacity)
    
    # Calculate net reserves
    net_reserves = total_installed_capacity - max_loads

    # If net_reserves is negative, set it to 0
    net_reserves = np.maximum(0, net_reserves)
    print("Net Reserves:" + str(net_reserves))
    
    # The fitness is the inverse of the net reserve
    fitness = 1.0 / np.sum(net_reserves)
    fitness_percentage = fitness * 100

    
    return fitness_percentage


fitness = fitness(chromosome, unitData, max_loads, totalcap)
print(f"Generated chromosome: ")
print(chromosome)
print ("Fitness: "+ str(fitness))