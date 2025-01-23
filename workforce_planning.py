import streamlit as st
import random
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus
import matplotlib.pyplot as plt
import pandas as pd

def solve_workforce_planning(weeks, hiring_cost, firing_cost, salary_cost, penalty_cost,
                              overtime_cost, initial_employees, maxh, maxf, overtime_rate,
                              working_hours, demand):
    # Define the problem
    problem = LpProblem("Workforce_Planning", LpMinimize)

    # Define the decision variables
    H = [LpVariable(f"H_{i}", lowBound=0, cat='Integer') for i in range(weeks)]
    F = [LpVariable(f"F_{i}", lowBound=0, cat='Integer') for i in range(weeks)]
    E = [LpVariable(f"E_{i}", lowBound=0, cat='Integer') for i in range(weeks)]
    O = [LpVariable(f"O_{i}", lowBound=0, cat='Integer') for i in range(weeks)]
    U = [LpVariable(f"U_{i}", lowBound=0, cat='Integer') for i in range(weeks)]

    # Objective Function
    problem += (lpSum(H[i]*hiring_cost + F[i]*firing_cost + E[i]*salary_cost +
                      O[i]*overtime_cost + U[i]*penalty_cost for i in range(weeks))), "Total_Cost"

    # Constraints
    for i in range(weeks):
        if i == 0:
            problem += E[i] == initial_employees + H[i] - F[i], f"Initial_{i}"
        else:
            problem += E[i] == E[i-1] + H[i] - F[i], f"Balance_{i}"

        # Demand constraint
        problem += E[i]*working_hours + O[i] + U[i] == demand[i], f"Demand_{i}"
        problem += H[i] <= maxh, f"Hiring_Capacity_{i}"
        problem += F[i] <= maxf, f"Firing_Capacity_{i}"
        problem += O[i] <= E[i] * overtime_rate, f"Overtime_{i}"
        problem += U[i] >= demand[i] - E[i] * working_hours - O[i], f"Unmet_Demand_{i}"

    # Solve the problem
    problem.solve()

    results = {
        "Status": LpStatus[problem.status],
        "Total Cost": problem.objective.value(),
        "Details": []
    }

    for i in range(weeks):
        results["Details"].append({
            "Week": i + 1,
            "Demand": demand[i],
            "Hired": H[i].value(),
            "Fired": F[i].value(),
            "Employees": E[i].value(),
            "Overtime": O[i].value(),
            "Unmet Demand": U[i].value()
        })

    return results

# Streamlit App
st.title("Workforce Planning Optimization")

# Input Fields
st.sidebar.header("Input Parameters")
weeks = st.sidebar.number_input("Number of Weeks", min_value=1, max_value=52, value=4)

hiring_cost = st.sidebar.number_input("Hiring Cost", value=100)
firing_cost = st.sidebar.number_input("Firing Cost", value=50)
salary_cost = st.sidebar.number_input("Salary Cost per Week", value=1000)
penalty_cost = st.sidebar.number_input("Penalty Cost for Unmet Demand", value=1000)
overtime_cost = st.sidebar.number_input("Overtime Cost per Hour", value=20)
initial_employees = st.sidebar.number_input("Initial Number of Employees", min_value=0, value=0)
maxh = st.sidebar.number_input("Maximum Hiring per Week", min_value=1, value=10)
maxf = st.sidebar.number_input("Maximum Firing per Week", min_value=1, value=5)
overtime_rate = st.sidebar.number_input("Overtime Rate per Employee (Hours)", min_value=1, value=10)
working_hours = st.sidebar.number_input("Working Hours per Employee per Week", min_value=1, value=40)

demand_range = st.sidebar.slider("Demand Range", min_value=10, max_value=500, value=(20, 200))
random_demand = st.sidebar.checkbox("Generate Random Demand", value=True)

if random_demand:
    demand = [random.randint(demand_range[0], demand_range[1]) for _ in range(weeks)]
else:
    demand = [st.sidebar.number_input(f"Demand for Week {i+1}", min_value=0, value=50) for i in range(weeks)]

# Solve and Display Results
if st.button("Optimize"):
    results = solve_workforce_planning(weeks, hiring_cost, firing_cost, salary_cost, penalty_cost,
                                       overtime_cost, initial_employees, maxh, maxf, overtime_rate,
                                       working_hours, demand)

    st.subheader("Optimization Results")
    st.write(f"Status: {results['Status']}")
    st.write(f"Total Cost: {results['Total Cost']}")

    # Convert results to DataFrame
    df = pd.DataFrame(results["Details"])
    st.write("Optimization Details:")
    st.dataframe(df)

    # Plot: Hired and Fired Employees vs. Week
    st.subheader("Hired and Fired Employees vs. Week")
    plt.figure(figsize=(10, 5))
    plt.bar(df['Week'], df['Hired'], label='Hired', color='green')
    plt.bar(df['Week'], df['Fired'], label='Fired', color='red')
    plt.xlabel('Week')
    plt.ylabel('Count')
    plt.title('Hired and Fired Employees per Week')
    plt.legend()
    st.pyplot(plt)

    # Plot: Overtime vs. Week
    st.subheader("Overtime Hours vs. Week")
    plt.figure(figsize=(10, 5))
    plt.bar(df['Week'], df['Overtime'], color='blue')
    plt.xlabel('Week')
    plt.ylabel('Overtime Hours')
    plt.title('Overtime Hours per Week')
    st.pyplot(plt)

    # Plot: Unmet Demand vs. Week
    st.subheader("Unmet Demand vs. Week")
    plt.figure(figsize=(10, 5))
    plt.bar(df['Week'], df['Unmet Demand'], color='orange')
    plt.xlabel('Week')
    plt.ylabel('Unmet Demand')
    plt.title('Unmet Demand per Week')
    st.pyplot(plt)

    # Plot: Total Workforce vs. Demand
    st.subheader("Total Workforce (Employees + Overtime) vs. Demand")
    total_workforce = df['Employees'] * working_hours + df['Overtime']
    plt.figure(figsize=(10, 5))
    plt.plot(df['Week'], total_workforce, label='Total Workforce', marker='o', color='green')
    plt.plot(df['Week'], df['Demand'], label='Demand', marker='x', color='red')
    plt.xlabel('Week')
    plt.ylabel('Workforce/Demand')
    plt.title('Total Workforce vs. Demand')
    plt.legend()
    st.pyplot(plt)
