# Workforce Planning Application

## Overview
The Workforce Planning Application optimizes workforce management decisions such as hiring, firing, and maintaining employees while minimizing costs. It uses **Linear Programming (LP)** to model and solve the problem, integrating constraints like hiring/firing limits, budget caps, demand satisfaction, overtime conditions, penalties for unmet demand, and service rates. The application is built with **PuLP** (a Python library for linear programming) for optimization and **Streamlit** for an interactive, web-based user interface.

Users can input parameters, view results in tabular format, and explore insights through visualizations. The app helps decision-makers design efficient workforce strategies and adjust inputs to explore various scenarios.  

👉 **Try the app here:** [Workforce Planning App](https://workforce-planning-scmzo5wmkrecgorpzupb3h.streamlit.app/)

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

---

## Mathematical Formulation

### **Indexes**
- $i$: Week index (1, 2, ..., $m$).

### **Parameters**
- $D_i$: Weekly demand (in hours) at week $i$.
- **Costs:**
  - `hiringC`: Cost to hire one employee per week.
  - `firingC`: Cost to fire one employee per week.
  - `salaryC`: Cost to maintain one employee per week.
  - `penaltyC`: Cost for unmet demand per week.
  - `overtimeC`: Cost of overtime hours per week.
- **Employee Details:**
  - `employees0`: Initial workforce at week 1.
  - `maxh`: Maximum number of employees that can be hired per week.
  - `maxf`: Maximum number of employees that can be fired per week.
  - `overtimeR`: Maximum overtime hours per employee.
  - `workingH`: Maximum regular working hours per employee.
- `budget`: Maximum budget available.
- `serviceR`: Fraction of demand that must be met each week.

### **Decision Variables**
- $H_i$: Number of employees hired in week $i$.
- $F_i$: Number of employees fired in week $i$.
- $E_i$: Number of employees maintained in week $i$.
- $O_i$: Total overtime hours in week $i$.
- $U_i$: Unmet demand (in hours) in week $i$.

### **Objective Function**:
Minimize the total cost:

$$
\min Z = \sum_{i=1}^{m} H_i \cdot \text{hiringC} + F_i \cdot \text{firingC} + E_i \cdot \text{salaryC} + O_i \cdot \text{overtimeC} + U_i \cdot \text{penaltyC}
$$

---

### **Constraints**:

1. **Employee Balance**:
   - For week 1:  
     $$
     E_1 = \text{employees0} + H_1 - F_1
     $$
   - For subsequent weeks (\(i > 1\)):  
     $$
     E_i = E_{i-1} + H_i - F_i
     $$

2. **Demand Satisfaction**:  
   Ensure sufficient workforce (including overtime and underutilization) to meet demand:  
   $$
   E_i \cdot {workingH + O_i + U_i \geq D_i \cdot serviceR
   $$

3. **Hiring and Firing Caps**:  
   Limit hiring and firing per week:  
   $$
   H_i \leq \text{maxh}, \quad F_i \leq \text{maxf}
   $$

4. **Overtime Limit**:  
   Restrict overtime hours to a percentage of total working hours:  
   $$
   O_i \leq E_i \cdot \text{overtimeR}
   $$

5. **Budget Constraint**:  
   Ensure total costs do not exceed the budget:  
   $$
   \sum_{i=1}^{m} H_i \cdot \text{hiringC} + F_i \cdot \text{firingC} + E_i \cdot \text{salaryC} + O_i \cdot \text{overtimeC} \leq \text{budget}
   $$
   
---

## How to Run Locally

