# Workforce Planning Application

## Overview
The Workforce Planning Application optimizes workforce management decisions such as hiring, firing, and maintaining employees while minimizing costs. It uses **Linear Programming (LP)** to model and solve the problem, integrating constraints like hiring/firing limits, budget caps, demand satisfaction, overtime conditions, penalties for unmet demand, and service rates. The application is built with **PuLP** (a Python library for linear programming) for optimization and **Streamlit** for an interactive, web-based user interface.

Users can input parameters, view results in tabular format, and explore insights through visualizations. The app helps decision-makers design efficient workforce strategies and adjust inputs to explore various scenarios.  

👉 **Try the app here:** [Workforce Planning App](https://workforce-planning-application-jc7bo3tnzssdn6pggcswif.streamlit.app/)

---

## Features

### 1. **User-Friendly Input Interface**
- Configure all parameters via the Streamlit sidebar:
  - **Costs:** Hiring, firing, salary, penalty, and overtime costs.
  - **Employee Details:** Initial workforce, maximum hiring/firing limits, working hours, and overtime rate.
  - **Budget and Demand:** Weekly budget cap, demand data, and service rate.
  - **Demand Data:** Choose between manually inputting demand or generating random demand within a specified range.

### 2. **Optimization Model**
The application solves a Linear Programming (LP) model with the following features:
- **Objective Function:** Minimize the total cost, which includes:
  - Hiring cost
  - Firing cost
  - Salary cost
  - Overtime cost
  - Penalty for unmet demand
- **Constraints:**
  - **Employee Balance:** Maintains continuity of workforce between weeks.
  - **Demand Satisfaction:** Meets weekly demand with a combination of regular workforce, overtime, and unmet demand allowance.
  - **Hiring/Firing Limits:** Caps on maximum hiring and firing per week.
  - **Overtime Limits:** Restricted overtime hours based on employee count.
  - **Unmet Demand Limits** Ensures the unmet demand is greater than or equal to the left demand after employees work and overtime.
  - **Budget Constraint:** Ensures total cost does not exceed the defined budget.

### 3. **Interactive Results and Visualizations**
- **Tabular Summary:** A detailed breakdown of weekly performance metrics:
  - Demand
  - Hiring and firing decisions
  - Employee count
  - Overtime hours
  - Unmet demand
- **Plots for Insightful Analysis:**
  - **Hired vs. Fired Employees:** A side-by-side bar chart to visualize weekly hiring and firing.
  - **Overtime vs. Unmet Demand:** A side-by-side bar chart comparison of how unmet demand is handled through overtime or left unaddressed.
  - **Total Workforce vs. Demand:** A line chart to analyze workforce capacity (including overtime) against demand.
  - **Cost Distribution Pie Chart:** An interactive pie chart showing the proportion of costs (hiring, firing, salary, overtime, and penalties).

## Mathematical Formulation

### **Indexes**
- $i$: Week index (1, 2, ..., $m$).

### **Parameters**
- $D_i$: Weekly demand (in hours) at week $i$.
- **Costs:**
  - `hiring_cost`: Cost to hire one employee per week.
  - `firing_cost`: Cost to fire one employee per week.
  - `salary_cost`: Cost to maintain one employee per week.
  - `penalty_cost`: Cost for unmet demand per week.
  - `overtime_cost`: Cost of overtime hours per week.
- **Employee Details:**
  - `initial_employees`: Initial workforce at week 1.
  - `maxh`: Maximum number of employees that can be hired per week.
  - `maxf`: Maximum number of employees that can be fired per week.
  - `overtime_rate`: Maximum overtime hours per employee.
  - `working_hours`: Maximum regular working hours per employee.
- `budget`: Maximum budget available.
- `service_rate`: Fraction of demand that must be met each week.

### **Decision Variables**
- $H_i$: Number of employees hired in week $i$.
- $F_i$: Number of employees fired in week $i$.
- $E_i$: Number of employees maintained in week $i$.
- $O_i$: Total overtime hours in week $i$.
- $U_i$: Unmet demand (in hours) in week $i$.

### **Objective Function**:
Minimize the total cost:

$$
\min Z = \sum_{i=1}^{m} H_i \cdot hiring_cost + F_i \cdot firing_cost + E_i \cdot salary_cost + O_i \cdot overtime_cost + U_i \cdot penalty_cost
$$

### **Constraints**:

1. **Employee Balance**:
- For week 1:  

$$ 
E_1 = initial_employees + H_1 - F_1 
$$

- For subsequent weeks $i > 1$:

$$ 
E_i = E_{i-1} + H_i - F_i 
$$

3. **Demand Satisfaction**:  
Ensure sufficient workforce (including overtime and underutilization) to meet demand:  

$$ 
E_i \cdot working_hours + O_i + U_i \geq D_i \cdot ServiceRate
$$

4. **Hiring and Firing Caps**:  
Limit hiring and firing per week:  

$$ 
H_i \leq maxh, \quad F_i \leq maxf 
$$

5. **Overtime Limit**:  
Restrict overtime hours to a percentage of total working hours:  

$$ 
O_i \leq E_i \cdot overtime_rate 
$$

6. **Unmet Demand Limit**
Ensure the Unmet Demand is larger than or equal to the remaining demand after the working hours and the overtime:

$$
U_i \geq D_i - E_i \cdot wokring_hours - O[i]
$$

8. **Budget Constraint**:  
Ensure total costs do not exceed the budget:  

$$ 
\sum_{i=1}^{m} H_i \cdot hiring_cost + F_i \cdot firing_cost + E_i \cdot salary_cost + O_i \cdot overtime_cost \leq budget 
$$
   
### Solving the Model:
The problem is solved using PuLP's LpProblem method, which uses available solvers (e.g., CBC) to find the optimal solution.

## How to Use:
1. Input the parameters
2. Click on "optimize" button

## Requirements:
- Python 3.x
- Streamlit
- Pandas
- PuLP
- Plotly

## Acknowledgments
- PuLP for Linear Programming formulation.
- Plotly for map visualization.
- Stramlit for web app deployment.
