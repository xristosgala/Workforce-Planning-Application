import streamlit as st
import random
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus
import pandas as pd
import altair as alt

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

        # Replace max with a conditional constraint for Overtime
        problem += O[i] <= E[i] * overtime_rate, f"Overtime_{i}"

        # Replace max with a conditional constraint for Unmet Demand
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
weeks = st.sidebar.number_input("Number of Weeks", min_value=1, value=4)

hiring_cost = st.sidebar.number_input("Hiring Cost", value=100)
firing_cost = st.sidebar.number_input("Firing Cost", value=50)
salary_cost = st.sidebar.number_input("Salary Cost", value=1000)
penalty_cost = st.sidebar.number_input("Penalty Cost for Unmet Demand", value=1000)
overtime_cost = st.sidebar.number_input("Overtime Cost", value=50)
initial_employees = st.sidebar.number_input("Initial Number of Employees", min_value=0, value=0)
maxh = st.sidebar.number_input("Maximum Hiring Number of Employees", min_value=1, value=10)
maxf = st.sidebar.number_input("Maximum Firing Number of Employees", min_value=1, value=5)
overtime_rate = st.sidebar.number_input("Overtime Rate per Employee", min_value=1, value=10)
working_hours = st.sidebar.number_input("Working Hours per Employee", min_value=1, value=40)

demand_range = st.sidebar.slider("Demand Range", min_value=10, max_value=1000, value=(20, 200))
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

    st.subheader("Details")

    # Convert results to a DataFrame for better visualization
    details_df = pd.DataFrame(results["Details"])
    
    # Display results as a table
    st.dataframe(details_df)
    
    # Line chart for demand, hired, fired, and employees
    st.subheader("Weekly Workforce Overview")
    chart = alt.Chart(details_df).transform_fold(
        ["Demand", "Hired", "Fired", "Employees"],
        as_=["Category", "Value"]
    ).mark_line().encode(
        x=alt.X("Week:O", title="Week"),
        y=alt.Y("Value:Q", title="Count"),
        color="Category:N",
        tooltip=["Week", "Category", "Value"]
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Bar chart for overtime and unmet demand
    st.subheader("Overtime and Unmet Demand")
    bar_chart = alt.Chart(details_df).transform_fold(
        ["Overtime", "Unmet Demand"],
        as_=["Category", "Value"]
    ).mark_bar().encode(
        x=alt.X("Week:O", title="Week"),
        y=alt.Y("Value:Q", title="Hours"),
        color="Category:N",
        tooltip=["Week", "Category", "Value"]
    ).interactive()

    
    st.altair_chart(bar_chart, use_container_width=True)
