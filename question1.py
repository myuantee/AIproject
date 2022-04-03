# imports libraries
from random import randint
import random
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Question 1: Vacation Planner")
st.markdown("Solving a vacation planning problem using Genetic Algorithm (GA). The goal is to optimize the vacation experience with a fixed amount of money and fixed duration. This application will generate the best combination of values for each parameter.")

st.markdown("Customize your **Money On-Hand** and **Duration** in the sidebar.")

st.sidebar.header("User Input")
budget = st.sidebar.slider("Money On-Hand (RM)", min_value = 1000, max_value = 10000, value = 1000, step = 1000)
duration = st.sidebar.slider("Duration (Day)", min_value = 1, max_value = 10, value = 3, step = 1)
p_count = st.sidebar.slider("Population", min_value = 100, max_value = 1000, value = 100, step = 100)
n_generation = st.sidebar.slider("Generation", min_value = 100, max_value = 1000, value = 200, step = 100)
data = {"Budget" : budget,
        "Duration" : duration,
        "population" : p_count,
        "n_generation" : n_generation}

budget = int(budget)
duration = int(duration)
p_count = int(p_count)
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

def objective(individual):
    return individual[0]*(duration - 1) + individual[1]*individual[2] + individual[3]*3*duration + individual[4]*individual[5]*duration

# calcultes average fitness of the population
def grade(pop):
    summed = [abs(objective(i) - budget) for i in pop]
    return (sum(summed) / len(pop))

# evolution function
def evolve(pop, retain, mutate, crossover1, crossover2, random_select = 0.05):
    
    graded = [(fitness(x), x) for x in pop]
    graded = [x[1] for x in sorted(graded)]  # x [1] because x has two component, just take the list --> e.g. [(50,[41,38,86,30,55])]
    fit = [x[0] for x in sorted(graded)]
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
            child = male[:crossover1] + female[crossover2:] # breeding
            children.append(child)
    parents.extend(children)
    
    return parents

def ga():
    # creates empty lists to store the results
    value_lst = []
    fitness_history = []
    value_list = []

    p = population(p_count)

    # starts to evolve
    for i in range(n_generation):
        p = evolve(p, retain, mutate, crossover1, crossover2)
        value = grade(p)
        fitness_history.append(value)
        value_lst.append(p[0])
        value_lst.append(value)

    # gets the final solution
    final_fit = value_lst[-1]
    solution_list = value_lst[-2]
    st.write("Final fitness score:", final_fit)
    
    # calculates sum of the values
    total = solution_list[0]*(duration - 1) + solution_list[1]*solution_list[2] + solution_list[3]*3*duration + solution_list[4]*solution_list[5]*duration
    st.write("Total vacation expenses: RM", total)

    parameter = ["Money On-Hand", "Vacation Duration", "Hotel Star Rating", "Tourist Spots", "One Tourist Spot",
                "Food Price", "Transportation Fees", "Transport Frequency"]
    value = [budget, duration]
    value.extend(solution_list[i] for i in range(len(solution_list)))

    # shows results in a dataframe
    df = pd.DataFrame(columns = ["Parameter" , "Value"])
    df.loc[0] = [parameter[0], "RM{}".format(value[0])]
    df.loc[1] = [parameter[1], "{} days".format(value[1])]
    df.loc[2] = [parameter[2], "< RM{} per night".format(value[2])]
    df.loc[3] = [parameter[3], "{} spots".format(value[3])]
    df.loc[4] = [parameter[4], "< RM{}".format(value[4])]
    df.loc[5] = [parameter[5], "< RM{} per meal".format(value[5])]
    df.loc[6] = [parameter[6], "< RM{} per trip".format(value[6])]
    df.loc[7] = [parameter[7], "{} trips per day".format(value[7])]

    styler = df.style.hide_index()
    st.write(styler.to_html(), unsafe_allow_html = True)

    # shows fitness history in dataframe
    hist_df = pd.DataFrame()
    hist_df["Generation"] = [x + 1 for x in list(range(len(fitness_history)))]
    hist_df["Fitness History"] = fitness_history

    return fitness_history, final_fit, hist_df

st.write("""---""")
st.subheader("Method Specifications")
table = pd.DataFrame()
table[" "] = ["Selection (%)", "Mutate Position", "From Male", "From Female"]
table["Method 1"] = ["30", "3", "first 3", "last 3"]
table["Method 2"] = ["50", "5", "first 1", "last 5"]
table["Method 3"] = ["10", "1", "first 2", "last 4"]

styler = table.style.hide_index()
st.write(styler.to_html(), unsafe_allow_html = True)

st.write("#")
st.subheader("Method 1")
retain = 0.2
mutate = 0.01
crossover1 = 3
crossover2 = 3
hist1, fit1, df1 = ga()

st.write("#")
st.subheader("Method 2")
retain = 0.5
mutate = 0.05
crossover1 = 1
crossover2 = 1
hist2, fit2, df2 = ga()

st.write("#")
st.subheader("Method 3")
retain = 0.1
mutate = 0.01
crossover1 = 2
crossover2 = 2
hist3, fit3, df3 = ga()

st.write("""---""")
st.subheader("Comparison of Results")

st.markdown("Comparing fitness history for each method.")
merged_df = pd.merge(df1, df2, how = "outer", on = ["Generation"])
merged_df = pd.merge(merged_df, df3, how = "outer", on = ["Generation"])
merged_df.columns = ["Generation", "Method 1", "Method 2", "Method 3"]
merged_df

st.write("#")
fig, ax = plt.subplots(figsize = (10, 5))

plt.plot(hist1, label = "Method 1")
plt.plot(hist2, label = "Method 2")
plt.plot(hist3, label = "Method 3")
plt.legend()

ax.set_xlabel("Generation")
ax.set_ylabel("Fitness")
ax.set_title("Fitness over Generation")
st.pyplot(fig)

fit_data = {"Method 1" : fit1,
           "Method 2" : fit2,
            "Method 3" : fit3}

plt.bar(list(fit_data.keys()), list(fit_data.values()))
plt.xlabel("Method")
plt.ylabel("Fitness")
plt.title("Fitness Score Comparison")

st.write("#")
fig, ax = plt.subplots(figsize = (10, 5))
plt.bar(list(fit_data.keys()), list(fit_data.values()))

ax.set_xlabel("Method")
ax.set_ylabel("Fitness")
ax.set_title("Final Fitness for Each Method")
st.pyplot(fig)
