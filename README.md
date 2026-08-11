# PyData_Capstone_Project

# Bank Customer Churn Analysis

## Project Overview

This project analyzes customer churn in a banking environment to understand why customers may leave and identify patterns that can support customer retention.

Using Python and PyData libraries, the project explores customer characteristics, account information, and product usage to compare customers who stayed with those who churned.

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

## Methodology

### 1. Data Collection

A banking customer dataset will be used containing customer demographic, account, and banking-related information, together with a customer churn indicator.

### 2. Data Cleaning and Preparation

The dataset will be inspected and prepared for analysis by:

- Checking for missing values
- Identifying and handling duplicates
- Checking data types
- Identifying inconsistent or invalid values
- Selecting relevant variables for the analysis

### 3. Exploratory Data Analysis

Customer characteristics and banking behavior will be explored using descriptive statistics.

The analysis will examine variables such as:

- Customer tenure
- Account balance
- Number of products
- Customer demographics
- Other relevant customer characteristics

### 4. Customer Churn Analysis

Customers who churned will be compared with customers who remained with the bank.

This will help identify patterns and characteristics associated with higher churn rates.

### 5. Data Visualization

Matplotlib and Seaborn will be used to create visualizations showing:

- Overall churn rates
- Churn across customer segments
- Relationships between customer characteristics and churn
- Differences between churned and retained customers

### 6. Insights and Recommendations

The findings will be summarized into key insights and practical recommendations that could help a bank improve customer retention.

---

## Tools & Libraries

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn

---

## Project Structure

```text
bank-customer-churn/
│
├── data/
│   └── customer_churn.csv
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   └── 03_churn_analysis.ipynb
│
├── README.md
└── requirements.txt