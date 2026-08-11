# PyData_Capstone_Project

# Bank Customer Churn Analysis

## Project Overview

This project analyzes customer churn in a banking environment to understand why customers may leave and identify patterns that can support customer retention.

Using Python and PyData libraries, the project explores customer characteristics, account information, and banking activity to compare customers who stayed with the bank with those who churned.

---

## Problem Statement

Customer churn can result in lost revenue and increased costs for banks. Understanding the characteristics and behaviors associated with churn can help banks identify customers who may be more likely to leave and develop targeted retention strategies.

This project aims to analyze customer data to identify patterns associated with churn and provide insights that can support better customer retention.

---

## Objectives

- Clean and prepare the customer dataset for analysis.
- Explore customer characteristics and banking behavior.
- Analyze patterns in customer churn.
- Identify customer characteristics associated with higher churn.
- Visualize key findings using clear and meaningful charts.
- Provide recommendations based on the findings.

---

## Key Questions

1. What proportion of customers have churned?
2. Which customer characteristics are most associated with churn?
3. Does the number of products a customer uses relate to churn?
4. Does customer tenure influence churn?
5. Are customers with higher account balances more or less likely to churn?
6. Which customer segments have the highest churn rates?

---

## Dataset

The project uses the **Churn Modelling** dataset, which contains information about bank customers and whether they exited the bank.

The dataset contains **10,000 customer records** and **14 variables**.

### Data Source

The dataset was obtained from Kaggle:

[Bank Customer Churn Dataset](https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling)

### Key Variables

| Variable | Description |
|---|---|
| CreditScore | Customer's credit score |
| Geography | Customer's country/region |
| Gender | Customer's gender |
| Age | Customer's age |
| Tenure | Number of years the customer has been with the bank |
| Balance | Customer's account balance |
| NumOfProducts | Number of banking products used |
| HasCrCard | Whether the customer has a credit card |
| IsActiveMember | Whether the customer is an active bank member |
| EstimatedSalary | Estimated customer salary |
| Exited | Whether the customer left the bank |

The `Exited` variable will be used as the main indicator of customer churn.

---

## Tools & Libraries

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn

---

## Methodology

### 1. Data Collection

The analysis uses the Churn Modelling dataset containing demographic, financial, and banking activity information for bank customers.

### 2. Data Cleaning and Preparation

The dataset will be inspected and prepared for analysis by:

- Checking for missing values
- Identifying duplicates
- Checking data types
- Identifying inconsistent or invalid values
- Removing variables that are not relevant to the analysis
- Preparing the data for exploratory analysis

### 3. Exploratory Data Analysis

Customer characteristics and banking behavior will be explored using descriptive statistics.

The analysis will focus on variables such as:

- Credit score
- Age
- Geography
- Gender
- Tenure
- Account balance
- Number of products
- Credit card ownership
- Active membership
- Estimated salary

### 4. Customer Churn Analysis

Customers who churned will be compared with customers who remained with the bank.

The analysis will examine how customer characteristics and banking behavior differ between the two groups.

### 5. Data Visualization

Matplotlib and Seaborn will be used to create visualizations showing:

- Overall churn rate
- Churn across customer segments
- Relationship between customer characteristics and churn
- Differences between churned and retained customers

### 6. Insights and Recommendations

The findings will be summarized into key insights and practical recommendations that could help a bank improve customer retention.

---
