from random import randint
import random
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import seaborn as sns

st.title("Question 1: Vacation Planner")
st.markdown("Solving a vacation planning problem using Genetic Algorithm (GA). The goal is to optimize the vacation experience with fixed amount of money and fixed duration. This application will generate the best combination of values for each parameter.")

st.markdown("Customize your **Money On-Hand** and **Duration** in the sidebar.")

st.sidebar.header("User Input")
budget = st.sidebar.selectbox("Money On-Hand (RM)", ("1000", "2000", "3000", "4000", "5000", "6000", "7000", "8000", "9000", "10000"))
duration =  st.sidebar.selectbox("Duration (Day)",("2", "3", "4", "5", "6", "7", "8", "9", "10"))
n_generation = st.sidebar.slider("Population", min_value = 100, max_value = 1000, value = 200)
data = {"Budget" : budget,
        "Duration" : duration,
        "n_generation" : n_generation}

budget = int(budget)
duration = int(duration)
n_generation = int(n_generation)

# creates a random initial individual (chromosome)
# specifies the range for each parameter, and incrementation
# returns individual as a list containing 6 numbers (genes)
def individual():
    hotel = random.randrange(50, 1000, 5)
    spots = random.randrange(2, 10)
    perspots = random.randrange(10, 500, 5)
    food = random.randrange(5, 100, 5)
    tfee = random.randrange(10, 200, 5)
    tfre = random.randrange(1, 10)
    
    return [hotel, spots, perspots, food, tfee, tfre]

# initializes the population
# returns population as a list containing COUNT individual 
def population(count):
    return [individual() for x in range(count)]

# creates a function to calculate the fitness score for each individual
# returns the distance between the sum of values and the budget
def fitness(individual):
    total = individual[0]*(duration - 1) + individual[1]*individual[2] + individual[3]*3*duration + individual[4]*individual[5]*duration
    return abs(budget - total)

# calcultes average fitness of the population
def grade(pop):
    summed = [fitness(i) for i in pop]
    return (sum(summed) / len(pop))

# evolution function
def evolve(pop, retain = 0.2, random_select = 0.05, mutate = 0.01):
    
    graded = [(fitness(x), x) for x in pop]
    graded = [x[1] for x in sorted(graded)]  # x [1] because x has two component, just take the list --> e.g. [(50,[41,38,86,30,55])]
    retain_length = int(len(graded)*retain) # how many top % parents to be remainded
    parents = graded[0:retain_length] # get the list of array of individuals as parents - after sorted

    # randomly adds other individuals to promote genetic diversity
    for individual in graded[retain_length:]: # gets from the remaining individuals NOT selected as parents initially
        if random_select > random.random():
            parents.append(individual)

    # mutates some individuals
    for individual in parents:
        if mutate > random.random():
            pos_to_mutate = randint(0, len(individual) - 1)
            individual[pos_to_mutate] = randint(min(individual), max(individual))

    # crossovers parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        if male != female: # makes sure two lists are different
            male = parents[male]
            female = parents[female]
            half = int(len(male)/2)
            child = male[:half] + female[half:] # breeding
            children.append(child)
    parents.extend(children)
    
    return parents

# creates empty lists to store the results
value_lst = []
fitness_history = []

p_count = 100

p = population(p_count)

# starts to evolve
for i in range(n_generation):
    p = evolve(p)
    value = grade(p)
    fitness_history.append(value)
    value_lst.append(p[0])
    value_lst.append(value)

solution_list = value_lst[-2]

solution_dict = {
            "Money on-hand" : budget,
            "Vacation duration" : duration,
            "Hotel star rating" : solution_list[0],
            "Tourist spots" : solution_list[1],
            "One tourist spot" : solution_list[2],
            "Food price" : solution_list[3],
            "Transportation fees" : solution_list[4],
            "Transport frequency" : solution_list[5],
            }

st.header("Solution")

total = solution_list[0]*(duration - 1) + solution_list[1]*solution_list[2] + solution_list[3]*3*duration + solution_list[4]*solution_list[5]*duration
st.write("Total vacation expenses: RM", total)

x_list = list(solution_dict.keys())
y_list = list(solution_dict.values())

df = pd.DataFrame(columns = ["Parameter" , "Value"])
df.loc[0] = [x_list[0], "RM{}".format(y_list[0])]
df.loc[1] = [x_list[1], "{} days".format(y_list[1])]
df.loc[2] = [x_list[2], "< RM{} per night".format(y_list[2])]
df.loc[3] = [x_list[3], "{} spots".format(y_list[3])]
df.loc[4] = [x_list[4], "< RM{}".format(y_list[4])]
df.loc[5] = [x_list[5], "< RM{} per meal".format(y_list[5])]
df.loc[6] = [x_list[6], "< RM{} per trip".format(y_list[6])]
df.loc[7] = [x_list[7], "{} trip per day".format(y_list[7])]

styler = df.style.hide_index()
st.write(styler.to_html(), unsafe_allow_html = True)

st.write("#")
st.header("Fitness History")
st.markdown("Adjust the **Population** in the sidebar and investgate the fitness history.")

# plot chart for findings
data =  {"fitness history": fitness_history} # assigns data of lists
fig, ax = plt.subplots(figsize = (10, 5))
ax = sns.lineplot(data = pd.DataFrame(data))
ax.set_xlabel("Population")
ax.set_ylabel("Fitness")
st.pyplot(fig)
