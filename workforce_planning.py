import streamlit as st
import random
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def solve_workforce_planning(weeks, hiring_cost, firing_cost, salary_cost, penalty_cost,
                              overtime_cost, initial_employees, maxh, maxf, overtime_rate,
                              working_hours, demand, budget, service_rate):
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
        problem += E[i]*working_hours + O[i] + U[i] >= demand[i] * service_rate, f"Demand_{i}"
        problem += H[i] <= maxh, f"Hiring_Capacity_{i}"
        problem += F[i] <= maxf, f"Firing_Capacity_{i}"
        problem += O[i] <= E[i] * overtime_rate, f"Overtime_{i}"
        problem += U[i] >= demand[i] - E[i] * working_hours - O[i], f"Unmet_Demand_{i}"
    
    # Budget constraint
    total_cost = lpSum(H[i]*hiring_cost + F[i]*firing_cost + E[i]*salary_cost +
                       O[i]*overtime_cost for i in range(weeks))
    problem += total_cost <= budget, "Budget_Constraint"

    # Solve the problem
    problem.solve()


    objective_cost = 0
    for i in range(weeks):
        objective_cost += U[i].value() * penalty_cost
      
    results = {
        "Status": LpStatus[problem.status],
        "Total Cost": problem.objective.value() - objective_cost,
        "cost": problem.objective.value(),
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
st.sidebar.header("Input Parameters per Week")
weeks = st.sidebar.number_input("Number of Weeks", min_value=1, max_value=52, value=4)

hiring_cost = st.sidebar.number_input("Hiring Cost", value=100)
firing_cost = st.sidebar.number_input("Firing Cost", value=50)
salary_cost = st.sidebar.number_input("Salary Cost", value=250)
penalty_cost = st.sidebar.number_input("Penalty for Unmet Demand", value=100)
overtime_cost = st.sidebar.number_input("Overtime Cost", value=75)
initial_employees = st.sidebar.number_input("Initial Number of Employees", min_value=0, value=0)
maxh = st.sidebar.number_input("Maximum Hiring", min_value=1, value=10)
maxf = st.sidebar.number_input("Maximum Firing", min_value=1, value=5)
overtime_rate = st.sidebar.number_input("Overtime Hours per Employee", min_value=1, value=10)
working_hours = st.sidebar.number_input("Working Hours per Employee", min_value=1, value=40)
budget = st.sidebar.number_input("Budget", min_value=0, value=10000)
demand_range = st.sidebar.slider("Demand Range", min_value=1, max_value=1000, value=(20, 200))
random_demand = st.sidebar.checkbox("Generate Random Demand", value=True)
service_rate = st.sidebar.slider("Service Rate", min_value=0.00, max_value=1.00, value=0.95)

if random_demand:
    demand = [random.randint(demand_range[0], demand_range[1]) for _ in range(weeks)]
else:
    demand = [st.sidebar.number_input(f"Demand for Week {i+1}", min_value=0, value=100) for i in range(weeks)]

# Solve and Display Results
if st.button("Optimize"):
    results = solve_workforce_planning(weeks, hiring_cost, firing_cost, salary_cost, penalty_cost,
                                       overtime_cost, initial_employees, maxh, maxf, overtime_rate,
                                       working_hours, demand, budget, service_rate)

    st.subheader("Optimization Results")
    if results['Status']=='Optimal':
        st.success(f"Status: {results['Status']}")
        st.write(f"Total Cost: {results['Total Cost']}")
        st.write(f"cost objective: {results['cost']}")
    
        # Convert results to DataFrame
        df = pd.DataFrame(results["Details"])
        st.write("Results in a Tabular Form:")
        st.dataframe(df)
    
        # Interactive Plot: Hired and Fired Employees vs. Week
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['Week'], y=df['Hired'], name='Hired', marker_color='green'))
        fig.add_trace(go.Bar(x=df['Week'], y=df['Fired'], name='Fired', marker_color='red'))
        fig.update_layout(barmode='group', xaxis_title='Week', yaxis_title='Count',
                          title='Hired vs Fired Employees per Week')
        st.plotly_chart(fig)
    
        # Interactive Plot: Overtime Employees vs Unmet Demand
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['Week'], y=df['Overtime'], name='Overtime', marker_color='blue'))
        fig.add_trace(go.Bar(x=df['Week'], y=df['Unmet Demand'], name='Unmet Demand', marker_color='orange'))
        fig.update_layout(barmode='group', xaxis_title='Week', yaxis_title='Count',
                          title='Overtime Employees vs Unmet Demand per Week')
        st.plotly_chart(fig)
    
        # Interactive Plot: Total Workforce vs. Demand
        df['Total Workforce'] = df['Employees'] * working_hours + df['Overtime']
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Week'], y=df['Total Workforce'], mode='lines+markers',
                                 name='Total Workforce', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=df['Week'], y=df['Demand'], mode='lines+markers',
                                 name='Demand', line=dict(color='red')))
        fig.update_layout(xaxis_title='Week', yaxis_title='Workforce/Demand',
                          title='Total Workforce (Employees + Overtime) vs. Demand', xaxis=dict(tickmode='array', tickvals=list(range(1, weeks+1))))
        st.plotly_chart(fig)
    
        # Assuming these are your calculated costs
        hiring_total_cost = sum(df['Hired']) * hiring_cost
        firing_total_cost = sum(df['Fired']) * firing_cost
        salary_total_cost = sum(df['Employees']) * salary_cost
        overtime_total_cost = sum(df['Overtime']) * overtime_cost
        penalty_total_cost = sum(df['Unmet Demand']) * penalty_cost
        
        # Calculate the total cost
        total_cost = (hiring_total_cost + firing_total_cost + salary_total_cost +
                      overtime_total_cost + penalty_total_cost)
        
        # Prepare data for the pie chart
        costs = [hiring_total_cost, firing_total_cost, salary_total_cost,
                 overtime_total_cost, penalty_total_cost]
        labels = ['Hiring Cost', 'Firing Cost', 'Salary Cost',
                  'Overtime Cost', 'Penalty Cost']
        
        # Create the pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=costs, textinfo='percent+label')])
        fig.update_layout(title='Cost Distribution')
        
        # Display the pie chart in Streamlit
        st.plotly_chart(fig)

    else:
        st.error(f"Status: {results['Status']}")
