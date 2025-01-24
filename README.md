# Workforce-Planning Application

## Overview
This application involves a Workforce Planning Problem using Linear Programming (LP) to optimize the decisions of hiring, firing and maintaining employees while minimizing costs. It integrates multiple constraints such as maximum number of hired and fired employees, budget limit, demand satisfaction, overtime condition and unmet demand limit, all to ensure that the planning system runs efficiently. The problem is solved using PuLP (a Python library for LP problems) and results are visualized using Streamlit for an interactive web-based experience. Additionally, the solution includes various plots allowing the user to gain informative insights. The app can be accessed via this link: [https://optimized-transportation-allocation-system-and-route-mapping.streamlit.app/](https://workforce-planning-scmzo5wmkrecgorpzupb3h.streamlit.app/)

## Features
**Data Input:** Users can input data from the left sidebar which includes number of weeks, hiring cost, firing cost, salary cost, penalty cost, overtime cost, initial number of employees, maximum hiring, maximumg firing, overtime hours, working hours, budget limit, demand data and service rate. .
**Optimization Model:** The system builds and solves a LP model that minimizes planning costs while satisfying all constraints (e.g., demand, budget, working hours, etc.).
**Visualizations:** Many plots are being created such as a simple summarization table, a bar plot between hired vs fired employees, a bar plot between overtime and unmet demand, a line plot of total workforce (employees + overtime) vs demand and last a costs distribution pie chart.
**Duals and Slacks:** Outputs the duals and slacks for each constraint to analyze the optimization.

## Mathematical Formulation (Linear Programming Model)

### Indexes
$i$ = number of weeks i.e. 1,2, \dots, m$

### Parameters
Let:

- $D_i$ is the demand (in hours) at week $i$, for $i = 1, 2, ... \dots, m$.
- hiring_cost is the cost of hiring one employee per week.
- firing_cost is the cost of firing one employee per week.
- salary_cost is the cost of maintaining one employee per week.
- penalty_cost is the cost of unmet demand per week.
- overtime_cost is the cost of overtime in hours per week.
- initial_employees is the starting number of employees at week 1.
- maximum_hiring is the maximum number of employees that can be hired each week.
- maximum_firing is the maximum number of employees that can be fired each week.
- overtime_horus is the maximum number of overtime hours that an employee can work each week.
- working_hours is the maximum number of working hours that an employee can work each week.
- budget_limit is the maximum budget available over all weeks.
- service_rate is the percentage number of customer service each week.

### Decision Variables:
- $H_{i}$: Integer decision variable representing the number of employees hired each week $i$.
- $F_{i}$: Integer decision variable representing the number of employees fired each week $i$.
- $E_{i}$: Integer decision variable representing the number of employees maintained each week $i$.
- $O_{i}$: Integer decision variable representing the number of overtime hours each week $i$.
- $U_{i}$: Integer decision variable representing the number of unmet demand each week $i$.

### Objective Function:
Minimize the total transportation cost:

$$
\min Z = \sum_{i=1}^{m} H_{i} \cdot hiring_cost + F_{i} \cdot firing_cost + E_{i} \cdot salary_cost + O_{i} \cdot overtime_cost + U{i} \cdot penalty_cost
$$

## Constraints:
1. **Maintained Employee Balance Constraints:**
   For week 1:
       Ensure that the total maintanted employees equal the initial number of employees plus the hired and fired ones:
$$
\E_{i} = initial_employees \cplus H_{i} \cminus F_{i} \quad \forall i
$$
   For week > 1:
   Ensure that the total maintanted employees equal the number of maintained employees from the previous week $i-1$ plus the hired and fired ones:
$$
\E_{i} = E_{i-1} \cdot H_{i} \cplus H_{i} \cminus F_{i} \quad \forall i
$$

2. **Demand Constraint**
   Ensure the employees remaining by the working hours plus the overtime hours and the unmet demand equals the demand times the service rate
   


