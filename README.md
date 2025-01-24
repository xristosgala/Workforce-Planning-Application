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
i = number of weeks i.e. 1,2,...,51,52.
