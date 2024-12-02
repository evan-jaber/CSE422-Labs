#Part: 1
import random

class GeneticAlgorithm:
    #This is the constrctor method to initialize the class
    def __init__(self, courses, num_of_courses, num_of_slots):
        self.courses = courses
        self.num_of_courses = num_of_courses
        self.num_of_slots = num_of_slots
        self.initial_population = []

    #This genarates a list of random values within 
    # the given range passed to the parameters to create a chromosome
    def genarate_random_val_arr(self, start, end):
        arr = []
        for i in range(self.num_of_courses*self.num_of_slots):
            var = random.randint(start, end)
            arr.append(var)
        return arr

    #This method calls the 'genarate_random_val_arr' method 
    # to genarate the chromosomes needed for the initial population
    def genarate_population(self, num_of_chromosomes):
        population = []
        for i in range (num_of_chromosomes):
            arr = self.genarate_random_val_arr(0, 1)
            population.append(arr)
        return population
    
    #This method calculates the fittness of the passed chromosome
    def calculate_fittness(self, chromosome):
        fittness = 0
        overlap_penalty = 0
        consistency_penalty = 0
        visited = []
        for i in range(self.num_of_courses):
            visited.append(0)
        for i in range(0, len(chromosome), self.num_of_courses):
            slot_filled= False
            for j in range(i, i+num_of_courses):
                if chromosome[j] == 1:
                    if not slot_filled:
                        slot_filled = True
                    else:
                        overlap_penalty += 1

                    if visited[j-i] == 0:
                        visited[j-i] = 1
                    elif visited[j-i] == 1:
                        consistency_penalty += 1
                        visited[j-i] = 2
        for i in (visited):
            if i == 0:
                overlap_penalty+=1
        fittness = -(overlap_penalty + consistency_penalty)
        return fittness
    
    #This method randomly chooses a chromosome from a population and returns it
    def selection(self, population):
        idx = random.randint(0, len(population)-1)
        return population[idx]
    
    #This method takes two parents as parameter and
    # returns two offsprings produced using single point crossover
    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, len(parent1)-1)
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
        return offspring1, offspring2
    
    #This method takes a chromosome as parameter and
    # it flips the value of a random index and returns the mutated chromosome
    def mutation(self, chromosome):
        mutation_idx = random.randint(0, len(chromosome)-1)
        chromosome[mutation_idx] = abs(chromosome[mutation_idx]-1)
        return chromosome
    
    #This method takes all the configurations to run the algorithm
    # such as number of chromosomes in a genaration and the max number of genarations the algo can run
    # Then it runs all the methods above to return the most optimal solution it got using the algorithm
    def run_algo(self, num_of_population, max_genarations):
        self.initial_population = self.genarate_population(num_of_population)
        current_population = self.initial_population
        next_population = []
        best_each_gen = []
        for i in range(max_genarations):
            for i in range (num_of_population//2):
                parent1 = self.selection(current_population)
                parent2 = self.selection(current_population)
                offspring1, offspring2 = self.crossover(parent1, parent2)
                offspring1 = self.mutation(offspring1)
                offspring2 = self.mutation(offspring2)
                next_population.append(offspring1)
                next_population.append(offspring2)

            best_fittness_value = self.calculate_fittness(next_population[0])
            fittest_chromosome = next_population[0]
            for i in range(len(next_population)):
                current_fittness_value = self.calculate_fittness(next_population[i])
                if current_fittness_value > best_fittness_value:
                    best_fittness_value = current_fittness_value
                    fittest_chromosome = next_population[i]
                elif current_fittness_value == 0:
                    return next_population[i], current_fittness_value, i
            
            best_each_gen.append(fittest_chromosome)
            current_population = next_population
            next_population = []

        fittest = best_each_gen[0]
        fittest_value = self.calculate_fittness(best_each_gen[0])
        for i in range(len(best_each_gen)):
            current_fittness_value = self.calculate_fittness(best_each_gen[i])
            if current_fittness_value > fittest_value:
                fittest_value = current_fittness_value
                fittest = best_each_gen[i]

        return fittest, fittest_value, max_genarations

#The below code block extracts data from input file and runs the 'GeneticAlgorithm' class
file_i = open('Assignment02_input.txt', 'r')
file_o = open('Assignment02_output.txt', 'w')
num_of_courses, num_of_slots = file_i.readline().split(' ')
num_of_courses, num_of_slots = int(num_of_courses), int(num_of_slots)
courses = []
for i in range (num_of_courses):
    courses.append(file_i.readline())

GA = GeneticAlgorithm(courses, num_of_courses, num_of_slots)
fittest, fittest_value, iterations = GA.run_algo(10, 100)

file_o.write(f"Part 1: \n Genaration: {iterations} \n Fittest Chromosome: {"".join(map(str, fittest))} \n Fittness: {fittest_value} \n\n")


#Part: 2
initial_population = GA.initial_population
def multipoint_crossover(parent1, parent2):
        crossover_point1 = random.randint(0, len(parent1)-2)
        crossover_point2 = random.randint(crossover_point1+1, len(parent1)-1)
        offspring1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
        offspring2 = parent2[:crossover_point1] + parent1[crossover_point1:crossover_point2] + parent2[crossover_point2:]
        return offspring1, offspring2, crossover_point1, crossover_point2

parent1 = initial_population[random.randint(0, len(initial_population)-1)]
parent2 = initial_population[random.randint(0, len(initial_population)-1)]
off1, off2, p1, p2 = multipoint_crossover(parent1, parent2)

#The below code block is used to format all the data and write to the output file
parent1 = "".join(map(str, parent1))
parent2 = "".join(map(str, parent2))
off1 = "".join(map(str, off1))
off2 = "".join(map(str, off2))

file_o.write(f"Part 2: \n Parent1: {parent1}, Parent2: {parent2} \n Crossover Points: {p1}, {p2} \n Offspring1: {off1}, Offspring2: {off2}")

file_i.close()
file_o.close()