import streamlit as st
import constraint
import pandas as pd  
import collections
import math

lst = [[20, 15, 10, 21, 5, 5000], 
       [30, 16, 15, 10, 2, 10000], 
       [22, 15, 11, 12, 3, 7500], 
       [16, 16, 16, 15, 1, 8500], 
       [19, 10, 20, 15, 1, 9500]]

state = [[1, 5000], [2, 10000], [3, 7500], [4, 8500], [5, 9500]]
state_pop = [[115900, 434890, 15000], [100450, 378860, 35234], [223400, 643320, 22318], [269300, 859900, 23893], [221100, 450500, 19284]]

for i in range(len(lst)):
    problem = constraint.Problem()

    problem.addVariable("CR1", range(lst[i][0] + 1))  
    problem.addVariable("CR2", range(lst[i][1] + 1))  
    problem.addVariable("CR3", range(lst[i][2] + 1))
    problem.addVariable("CR4", range(lst[i][3] + 1))
    problem.addVariable("CR5", range(lst[i][4] + 1))

    # max capacity for states
    def state_max(a, b, c, d, e):  
        if (a*200 + b*500 + c*1000 + d*2500 + e*4000) == lst[i][5]:
            return True

    problem.addConstraint(state_max,["CR1", "CR2", "CR3", "CR4", "CR5"])

    min_rental = 99999999 
    solution_found = {}  
    solutions = problem.getSolutions()

    # gets the conditions with minimum rental
    for s in solutions:
        current_rental = s["CR1"]*100 + s["CR2"]*250 + s["CR3"]*500 + s["CR4"]*800 + s["CR5"]*1200
        if current_rental < min_rental:
            min_rental = current_rental
            solution_found = s
    
    od = collections.OrderedDict(sorted(solution_found.items()))
    df = pd.DataFrame(od.items())
    df3 = df.rename(columns = {0 : "Centre", 1 : "Number of Centres Needed"})

    subheader = "State {}".format(i + 1)
    st.subheader(subheader)

    st.write("Maximum vaccination capacity per day in this state is", state[i][1])
    st.write("Population of state:", sum(state_pop[i]))
    
    st.write(df3)

    df2 = pd.DataFrame()
    df2["Age"] = ["< 35", "35 to 60", "> 60"]
    df2["Population"] = state_pop[i]
    df2["Vaccine Type"] = ["VacA", "VacB", "VacC"]
    
    vacA = math.ceil(state_pop[i][2] / state[i][1])
    vacB = math.ceil(state_pop[i][1] / state[i][1])
    vacC = math.ceil(state_pop[i][0] / state[i][1])
    
    df2["Number of Days"] = [vacA, vacB, vacC]
    
    st.write(df2)
    
    total = vacA + vacB + vacC
    st.write("\nTotal number of days to assign all vaccines:", total, "days")
    st.write("Rental per day: RM", min_rental)