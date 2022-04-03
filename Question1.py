from random import randint
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st

## test test
##code for streamlit

st.write("""
# Genetic Algorithm Application




""")

st.sidebar.header('User input')


budget = st.sidebar.selectbox('Budget',('3000','4000','5000','6000','7000','8000'))
duration =  st.sidebar.selectbox('Duration(Days)',('3','4','5','6','7','8'))
data = {'Budget': budget,
        'Duration': duration}
    


## Question 1

budget = int(budget)
duration = int(duration)

def individual():
    hotel = random.randrange(50, 1000, 5)
    spots = random.randrange(2, 10)
    perspots = random.randrange(10, 500, 5)
    food = random.randrange(5, 100, 5)
    tfee = random.randrange(10, 200, 5)
    tfre = random.randrange(1, 10)
    
    return [hotel, spots, perspots, food, tfee, tfre]
 
def population(count):
    return [individual() for x in range(count)]

def fitness(individual):
    total = individual[0]*(duration - 1) + individual[1]*individual[2] + individual[3]*3*duration + individual[4]*individual[5]*duration
    return abs(budget - total)

def grade(pop):
    summed = [fitness(i) for i in pop]
    return (sum(summed) / len(pop))


# Evolution function

def evolve(pop, retain = 0.2, random_select = 0.05, mutate = 0.01):
    
  
    graded = [(fitness(x), x) for x in pop]
    graded = [x[1] for x in sorted(graded)]  # x [1] because x has two component, just take the list --> e.g. [(50,[41,38,86,30,55])]
    retain_length = int(len(graded)*retain) # how many top % parents to be remainded
    parents = graded[0:retain_length] # get the list of array of individuals as parents - after sorted

    # randomly add other individuals to promote genetic diversity
    for individual in graded[retain_length:]: # get from the remaining individuals NOT selected as parents initially !
        if random_select > random.random():
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate > random.random():
            pos_to_mutate = randint(0, len(individual) - 1)
            individual[pos_to_mutate] = randint(min(individual), max(individual))

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = int(len(male)/2)
            child = male[:half] + female[half:]
            children.append(child)
    parents.extend(children)
    
    return parents


value_lst = []
fitness_history = []

p_count = 100
n_generation = 200

p = population(p_count)

#start to evolve
for i in range(n_generation):
    p = evolve(p)
    value = grade(p)
    fitness_history.append(value)
    value_lst.append(p[0])
    value_lst.append(value)

#plot chart for findings

data =  {"fitness history": fitness_history,"individual" : np.arange(1,201)} # assigns data of lists

# print("value list :",value_lst)
# print("\n")
# print("value list for test:",value_lst[::2])
# print("\n")
# print("fitness :",fitness_history)
# print("\n")
# print("population :",p)

df = pd.DataFrame(data) # creates dataframe 
df.index = range(1, df.shape[0] + 1) # starts the dataframe index with 1

df.plot(figsize=(10, 5))
plt.title("Fitness history")
plt.xlabel("number of individual")
plt.ylabel("fitness")
st.line_chart(df)


##show solutions

# parameter = ["Money on-hand", "Vacation duration", "Hotel star rating", "Tourist spots",
#             "One tourist spot", "Food price", "Transportation fees", "Transport frequency"]
# value_lst[-2]


solution = {
            "Money on-hand " : budget,
            "Vacation duration " : duration,
            "Hotel star rating " : value_lst[-2][0],
            "Tourist spots" : value_lst[-2][1],
            "One tourist spot" : value_lst[-2][2],
            "Food price" : value_lst[-2][3],
            "Transportation fees" : value_lst[-2][4],
            "Transport frequency" : value_lst[-2][5],
            }

st.write("# Vacation Planner")
individual = value_lst[-2]
total = individual[0]*(duration - 1) + individual[1]*individual[2] + individual[3]*3*duration + individual[4]*individual[5]*duration
total

x_list = list(solution.keys())
y_list =list(solution.values())



# solutiondict = {'Parameters': x_list,'Values':y_list}
# df = pd.DataFrame('Parameters':x,'Value':)
df = pd.DataFrame({'Parameters':x_list,
                    'Values':y_list})


styler = df.style.hide_index()

st.write(styler.to_html(), unsafe_allow_html=True)



