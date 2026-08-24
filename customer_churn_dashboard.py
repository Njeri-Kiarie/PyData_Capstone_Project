import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

customer_data = pd.read_csv("cleaned_churn_data.csv")

customer_data["AgeGroup"] = pd.cut(customer_data["Age"],
    bins=[0, 25, 35, 45, 55, 65, float("inf")],
    labels=["18-25", "26-35", "36-45", "46-55", "56-65", "66+"]
)

customer_data['BalanceGroup'] = pd.cut(customer_data['Balance'],
    bins=[-1, 50000, 100000, 150000, 200000, float('inf')],
    labels=['0–50K', '50K–100K', '100K–150K', '150K–200K', '200K+']
)

customer_data['CreditScoreGroup'] = pd.cut(customer_data['CreditScore'],
    bins=[300, 500, 600, 700, 800, 850],
    labels=['350–499', '500–599', '600–699', '700–799', '800–850']
)

customer_data['SalaryGroup'] = pd.cut(customer_data['EstimatedSalary'],
    bins=[0, 50000, 100000, 150000, 200000],
    labels=['0–50K', '50K–100K', '100K–150K', '150K–200K']
)

# ============================================================
# DASHBOARD TITLE
# ============================================================

st.title("📊 Bank Customer Churn Analysis Dashboard")

# ============================================================
# PROJECT OVERVIEW
# ============================================================

with st.expander("Project Overview", expanded=True):

    st.markdown("""
    ### About the Project

    This project analyzes customer churn in a banking environment to understand 
    why customers may leave and identify patterns that can support customer retention.

    Using Python and PyData libraries, the project explores customer characteristics, 
    account information, and banking activity to compare customers who stayed with the 
    bank with those who churned.
     
    ### Problem Statement

    Customer churn can result in lost revenue and increased costs for banks. 
    Understanding the characteristics and behaviors associated with churn can 
    help banks identify customers who may be more likely to leave and develop 
    targeted retention strategies.
    
    This project aims to analyze customer data to identify patterns associated with 
    churn and provide insights that can support better customer retention.

    ### Key Questions

    1. What proportion of customers have churned?
    2. Which customer characteristics are most associated with churn?
    3. Does the number of products a customer uses relate to churn?
    4. Does customer tenure influence churn?
    5. Are customers with higher account balances more or less likely to churn?
    6. Which customer segments have the highest churn rates?
    7. Does customer activity level influence the likelihood of churn?
    8. Does churn differ across countries?

    ### Dataset

    The project uses the **Churn Modelling** dataset, which contains information 
    about bank customers and whether they exited the bank.

    The dataset contains **10,000 customer records** and **14 variables**.

    The customers in the dataset are from three countries:

    - France
    - Spain
    - Germany

    ### Data Source
    The dataset was obtained from Kaggle: [Bank Customer Churn Dataset](https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling)

    ### Key Variables

    The `Exited` variable will be used as the main indicator of customer churn:

    - `0` = Customer stayed with the bank
    - `1` = Customer exited the bank

    """)

st.markdown(
    "An interactive analysis of customer churn patterns and high-risk segments."
)


# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("Filters")

geography = st.sidebar.multiselect(
    "Select Geography",
    options=sorted(customer_data["Geography"].unique()),
    default=sorted(customer_data["Geography"].unique())
)

age_group = st.sidebar.multiselect(
    "Select Age Group",
    options=sorted(customer_data["AgeGroup"].unique()),
    default=sorted(customer_data["AgeGroup"].unique())
)

num_products = st.sidebar.multiselect(
    "Number of Products",
    options=sorted(customer_data["NumOfProducts"].unique()),
    default=sorted(customer_data["NumOfProducts"].unique())
)


# Error handling
try:

    filtered_data = customer_data.copy()

    if geography:
        filtered_data = filtered_data[
            filtered_data["Geography"].isin(geography)
        ]

    if age_group:
        filtered_data = filtered_data[
            filtered_data["AgeGroup"].isin(age_group)
        ]

    if num_products:
        filtered_data = filtered_data[
            filtered_data["NumOfProducts"].isin(num_products)
        ]

    if filtered_data.empty:
        st.warning(
            "No customers match the selected filters. "
            "Please adjust your filters and try again."
        )

    else:
        pass
        
except KeyError as e:
    st.error(f"Missing column in the dataset: {e}")

except TypeError as e:
    st.error(f"Invalid data type encountered: {e}")

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

# ============================================================
# FILTER DATA
# ============================================================

filtered_data = customer_data[
    (customer_data["Geography"].isin(geography))
    & (customer_data["AgeGroup"].isin(age_group))
    & (customer_data["NumOfProducts"].isin(num_products))
]


# ============================================================
# DASHBOARD MENU
# ============================================================

menu1, menu2, menu3 = st.tabs([
    "Churn Overview",
    "Segmented Analysis",
    "Insights & Recommendations"
])


# ============================================================
# OVERVIEW TAB
# ============================================================

with menu1:
    # =========================
    # KPI METRICS
    # =========================

    total_customers = len(filtered_data)

    churned_customers = filtered_data["Exited"].sum()

    churn_rate = filtered_data["Exited"].mean() * 100

    stayed_customers = len(
        filtered_data[filtered_data["Exited"] == 0]
    )


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Customers",
            f"{total_customers:,}"
        )

    with col2:
        st.metric(
            "Churned Customers",
            f"{churned_customers:,}"
        )

    with col3:
        st.metric(
            "Churn Rate",
            f"{churn_rate:.2f}%"
        )

    with col4:
        st.metric(
            "Stayed Customers",
            f"{stayed_customers:,}"
        )

    # =========================
    # CHURN DISTRIBUTION
    # =========================
    st.subheader("Overall Churn Distribution")

    churn_counts = (filtered_data["Exited"].value_counts().reindex([0, 1], fill_value=0))

    churn_counts.index = ["Stayed", "Churned"]

    fig = px.pie(
        values=churn_counts.values,
        names=churn_counts.index,
        hole=0.5,
        title="Customer Churn Distribution"
    )

    fig.update_traces(
        textinfo="percent+label",
        marker=dict(
            colors=["#00A6A6", "#E63946"]
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # ============================================================
    # CHURN RATE BY GEOGRAPHY
    # ============================================================

    st.subheader("Churn Rate by Geography")

    churn_by_geography = (
        filtered_data.groupby("Geography")["Exited"].mean().mul(100).reset_index().round(2))

    fig = px.bar(
        churn_by_geography,
        x="Geography",
        y="Exited",
        text="Exited",
        title="Churn Rate by Geography"
    )

    fig.update_traces(
        marker_color="#E63946",
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Churn Rate (%)",
        yaxis_range=[0, 40]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # CHURN RATE BY AGE GROUP
    # ============================================================

    st.subheader("Churn Rate by Age Group")

    churn_age = (
        filtered_data.groupby("AgeGroup", observed=True)["Exited"].mean().mul(100).reset_index().round(2))

    fig = px.bar(
        churn_age,
        x="AgeGroup",
        y="Exited",
        text="Exited",
        title="Churn Rate by Age Group"
    )

    fig.update_traces(
        marker_color="#E63946",
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Churn Rate (%)",
        yaxis_range=[0, 60]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # CHURN RATE BY TENURE
    # ============================================================

    st.subheader("Churn Rate by Tenure")

    churn_tenure = (
        filtered_data.groupby("Tenure")["Exited"].mean().mul(100).reset_index().round(2))

    fig = px.bar(
        churn_tenure,
        x="Tenure",
        y="Exited",
        text="Exited",
        title="Churn Rate by Tenure"
    )

    fig.update_traces(
            marker_color="#E63946",
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )
    
    fig.update_layout(
        xaxis_title="Tenure (Years)",
        yaxis_title="Churn Rate (%)",
        yaxis_range=[0, 30]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # CHURN RATE BY MEMBERSHIP ACTIVITY
    # ============================================================

    st.subheader("Churn Rate by Membership Activity")

    activity_churn = (
        filtered_data.groupby("IsActiveMember")["Exited"].mean().mul(100).reset_index().round(2)
    )

    activity_churn["Membership"] = activity_churn["IsActiveMember"].map({
        0: "Inactive",
        1: "Active"
    })

    fig = px.bar(
        activity_churn,
        x="Membership",
        y="Exited",
        text="Exited",
        title="Churn Rate by Membership Activity"
    )

    fig.update_traces(
        marker_color=["#E63946", "#00A6A6"],
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Membership Status",
        yaxis_title="Churn Rate (%)",
        yaxis_range=[0, 35]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # CHURN RATE BY NUMBER OF PRODUCTS
    # ============================================================

    st.subheader("Churn Rate by Number of Products")

    product_churn = (
        filtered_data.groupby("NumOfProducts")["Exited"].mean().mul(100).reset_index().round(2)
    )

    fig = px.line(
        product_churn,
        x="NumOfProducts",
        y="Exited",
        markers=None,
        title="Churn Rate by Number of Products"
    )

    fig.update_traces(
        line_color="#E63946",
        marker_color="#E63946"
    )

    fig.update_layout(
        xaxis_title="Number of Products",
        yaxis_title="Churn Rate (%)",
        yaxis_range=[0, 110],
        xaxis=dict(dtick=1)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # CHURN RATE BY ACCOUNT BALANCES
    # ============================================================
    st.subheader("Churn Rate by Account Balance")
    
    churn_balance = (
        filtered_data.groupby("BalanceGroup")["Exited"].mean().mul(100).reset_index().round(2))
    
    fig = px.bar(
        churn_balance,
        x="BalanceGroup",
        y="Exited",
        text="Exited",
        title="Churn Rate by Account Balances"
    )
    
    fig.update_traces(
        marker_color="#E63946",
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )
        
    fig.update_layout(
        xaxis_title="Balance Group",
        yaxis_title="Churn Rate (%)",
        yaxis_range=[0, 60]
    )
    
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # CHURN RATE BY CREDIT CARD OWNERSHIP
    # ============================================================
    st.subheader("Churn Rate by Credit Card Ownership")
    
    churn_credit_card = (
        filtered_data.groupby("HasCrCard")["Exited"].mean().mul(100).reset_index().round(2))

    churn_credit_card["HasCrCard"] = churn_credit_card["HasCrCard"].map({
            0: "No",
            1: "Yes"
        })
    
    fig = px.bar(
        churn_credit_card,
        x="HasCrCard",
        y="Exited",
        text="Exited",
        title="Churn Rate by Credit Card Ownership"
    )
    
    fig.update_traces(
        marker_color="#E63946",
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )
        
    fig.update_layout(
        xaxis_title="Credit Card",
        yaxis_title="Churn Rate (%)",
        yaxis_range=[0, 25]
    )
    
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # CHURN RATE BY SALARY
    # ============================================================
    st.subheader("Churn Rate by Salary")
        
    churn_salary = (
        filtered_data.groupby("SalaryGroup")["Exited"].mean().mul(100).reset_index().round(2))
        
    fig = px.bar(
        churn_salary,
        x="SalaryGroup",
        y="Exited",
        text="Exited",
        title="Churn Rate by Estimated Salary"
    )
        
    fig.update_traces(
        marker_color="#E63946",
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )
            
    fig.update_layout(
        xaxis_title="Estimated Salary",
        yaxis_title="Churn Rate (%)",
        yaxis_range=[0, 25]
    )
        
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # CHURN RATE BY CREDIT SCORE
    # ============================================================
    st.subheader("Churn Rate by Credit Score")
    
    churn_credit_score = (
        filtered_data.groupby("CreditScoreGroup")["Exited"].mean().mul(100).reset_index().round(2))
    
    fig = px.bar(
        churn_credit_score,
        x="CreditScoreGroup",
        y="Exited",
        text="Exited",
        title="Churn Rate by Credit Score"
    )
    
    fig.update_traces(
        marker_color="#E63946",
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )
        
    fig.update_layout(
        xaxis_title="Credit Score Group",
        yaxis_title="Churn Rate (%)",
        yaxis_range=[0, 30]
    )
    
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    
with menu2:
    # ============================================================
    # SEGMENT ANALYSIS TAB
    # ============================================================
    st.markdown(
        "Explore how churn varies across combinations of customer characteristics."
    )

    # ============================================================
    # AGE × MEMBERSHIP ACTIVITY
    # ============================================================

    st.subheader("1. Churn Rate by Age and Membership Activity")

    age_activity = (filtered_data.groupby(["AgeGroup", "IsActiveMember"],observed=True)["Exited"]
        .mean()
        .mul(100)
        .reset_index()
        .round(2)
    )

    age_activity["Membership"] = age_activity["IsActiveMember"].map({
        0: "Inactive",
        1: "Active"
    })

    fig = px.bar(
        age_activity,
        x="AgeGroup",
        y="Exited",
        color="Membership",
        barmode="group",
        text="Exited",
        title="Churn Rate by Age Group and Membership Activity",
        color_discrete_map={
            "Inactive": "#E63946",
            "Active": "#00A6A6"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Churn Rate (%)",
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # HIGH-RISK INSIGHT
    # ============================================================

    st.markdown("### Key Insight")

    st.info(
        "Older inactive customers show particularly high churn rates. "
        "The exploratory analysis identified the 46–55 and 56–65 age groups "
        "as especially high-risk, with inactive customers showing substantially "
        "higher churn than active customers."
    )

    # ========================================================
    # GEOGRAPHY × AGE
    # ========================================================

    st.subheader("2. Churn Rate by Age and Geography")
    churn_geo_age = (
        filtered_data
        .groupby(["Geography", "AgeGroup"])["Exited"]
        .mean()
        .mul(100)
        .reset_index()
        .round(2)
    )

    # Convert to matrix for heatmap
    heatmap_data = churn_geo_age.pivot(
        index="Geography",
        columns="AgeGroup",
        values="Exited"
    )

    # Keep age groups in the correct order
    age_order = ["18-25", "26-35", "36-45", "46-55", "56-65", "66+"]

    heatmap_data = heatmap_data.reindex(columns=age_order)

    fig = px.imshow(
        heatmap_data,
        text_auto=".1f",
        color_continuous_scale="Reds",
        aspect="auto",
        labels={
            "x": "Age Group",
            "y": "Geography",
            "color": "Churn Rate (%)"
        },
        title="Customer Churn Rate by Age and Geography"
    )

    fig.update_layout(
        title_font_size=24,
        xaxis_title="Age Group",
        yaxis_title="Geography",
        coloraxis_colorbar_title="Churn Rate (%)",
        margin=dict(t=70, l=60, r=40, b=50)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("**Insight:**")
    st.info(
        "Churn increases substantially among older customers across the "
        "three countries, with the highest churn concentrated in the "
        "46–65 age groups."
    )

    # ============================================================
    # AGE × MEMBERSHIP ACTIVITY
    # ============================================================
    st.subheader("3. Churn Rate by Age and Membership Activity")
        
    churn_age_activity = (
        filtered_data
        .groupby(["AgeGroup", "IsActiveMember"], observed=True)["Exited"]
        .mean()
        .mul(100)
        .reset_index()
    )
        
    churn_age_activity["Membership Status"] = churn_age_activity[
        "IsActiveMember"
        ].map({
        0: "Inactive",
        1: "Active"
    })
        
    fig = px.bar(
        churn_age_activity,
        x="AgeGroup",
        y="Exited",
        color="Membership Status",
        color_discrete_map={
            "Inactive": "#D9534F",
            "Active": "#2E86AB"
            },
        text="Exited",
        title="Churn Rate by Age and Membership Activity"
        )
        
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )
        
    fig.update_layout(
        barmode="group",
        xaxis_title="Age Group",
        yaxis_title="Churn Rate (%)",
        legend_title="Membership Status"
    )
        
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("**Key Insight:**")

    st.info("""
        Inactive customers have consistently higher churn rates than active customers, 
        with the largest differences among customers aged 46–65. The 56–65 inactive 
        group has the highest observed churn, making older inactive customers a key 
        high-risk segment for retention efforts.
    """)
    
    # ========================================================
    # GEOGRAPHY × TENURE
    # ========================================================
    st.subheader("4. Churn Rate by Geography and Tenure")

    churn_geo_tenure = (
        filtered_data
        .groupby(["Geography", "Tenure"])["Exited"]
        .mean()
        .mul(100)
        .reset_index()
    )

    fig = px.line(
        churn_geo_tenure,
        x="Tenure",
        y="Exited",
        color="Geography",
        markers=None,
        title="Churn Rate by Geography and Tenure",
        color_discrete_map={
            'France': '#2E86AB',
            'Germany': '#E63946',
            'Spain':  '#F58518'
        }
    )

    fig.update_layout(
        xaxis_title="Tenure (Years)",
        yaxis_title="Churn Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("**Key Insight:**")
    st.info(
        "Customers with longer tenure generally show higher churn in the "
        "older customer segments, suggesting that retention efforts should "
        "not focus only on newly acquired customers."
    )


    # ============================================================
    # 3. PRODUCTS AND MEMBERSHIP ACTIVITY
    # ============================================================

    st.subheader("5. Products and Membership Activity")

    if "Membership Status" not in filtered_data.columns:
        filtered_data = filtered_data.copy()

        filtered_data["Membership Status"] = filtered_data["IsActiveMember"].map({
        0: "Inactive",
        1: "Active"
    })

    # Calculate churn rate by number of products and membership status
    churn_products_activity = (
        filtered_data
        .groupby(["NumOfProducts", "Membership Status"])["Exited"]
        .mean()
        .mul(100)
        .reset_index()
        .round(2)
    )

    # Create line chart
    fig = px.line(
        churn_products_activity,
        x="NumOfProducts",
        y="Exited",
        color="Membership Status",
        markers=None,
        title="Customer Churn Rate by Number of Products and Membership Activity",
        labels={
            "NumOfProducts": "Number of Products",
            "Exited": "Churn Rate (%)",
            "Membership Status": "Membership Status"
        },
        color_discrete_map={
            "Inactive": "#D9534F",
            "Active": "#2E86AB"
        }
    )

    # Display churn percentage on hover
    fig.update_traces(
        hovertemplate=(
            "<b>Number of Products: %{x}</b><br>"
            "Churn Rate: %{y:.1f}%"
            "<extra></extra>"
        )
    )

    # Chart formatting
    fig.update_layout(
        title_font_size=24,
        xaxis_title="Number of Products",
        yaxis_title="Churn Rate (%)",
        legend_title="Membership Status",
        hovermode="x unified",
        margin=dict(
            t=70,
            l=60,
            r=40,
            b=50
        )
    )

    # Display chart
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # INSIGHT
    # ============================================================

    st.markdown("### Key Insight")

    st.info(
        """
        Customers with 3 or 4 products show unusually high observed churn
        compared with customers holding fewer products. However, these
        groups contain relatively few customers, so the result should be
        treated as a signal for further investigation rather than a
        definitive conclusion.

        Membership activity provides additional context, with inactive
        customers generally showing higher churn than active customers.
        """
    )
    


with menu3:
    # ========================================================
    # KEY INSIGHTS
    # ========================================================

    st.subheader("Key Insights")

    st.markdown("""
    ### 1. Age is a major churn differentiator

    Customers aged between **46–65** have substantially higher churn rates
    than younger customers. The **46–55** age group reached approximately
    **50.6%**, while the **56–65** age group recorded about **48.3%** overall.
    """)

    st.markdown("""
    ### 2. Inactive customers are much more likely to churn

    Overall churn was **26.85%** for inactive customers compared with
    **14.27%** for active customers. This pattern was also observed across
    countries and age groups.
    """)

    st.markdown("""
    ### 3. Germany is the highest-risk geography

    Germany had an overall churn rate of approximately **32.4%**, compared
    with **16.2%** in France and **16.7%** in Spain.
    """)

    st.markdown("""
    ### 4. Number of products shows an unusual relationship with churn

    Customers with **3 or 4 products** have exceptionally high observed
    churn. However, these groups are small, so this finding should be treated
    as a signal requiring further investigation rather than a definitive
    conclusion.
    """)

    st.markdown("""
    ### 5. Short-tenure customers require attention

    The tenure analysis showed elevated churn among customers at the
    beginning of their relationship, particularly at **0 years**. This
    suggests that early customer experience and onboarding may be important
    areas worth investigating.
    """)

    st.markdown("""
    ### 6. Balance can distinguish some high-risk customers

    The **200K balance group** recorded **55.88%** churn, but contained only
    **34 customers**. The result is therefore interesting but should not be
    treated as a strong generalizable conclusion.
    """)

    st.markdown("""
    ### 7. Some variables appear relatively weak

    Estimated Salary and credit-card ownership showed only small differences
    in churn. Credit-card ownership had **20.81%** churn compared with
    **20.18%** for customers without it, suggesting little separation between
    the two groups.
    """)

    st.divider()

    # ========================================================
    # OVERALL HIGH-RISK SEGMENT
    # ========================================================

    st.info(
        "Older, inactive customers — particularly those aged 46–65 — "
        "represent a high-risk churn segment, with Germany showing especially "
        "high churn among these age groups."
    )

    st.divider()

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.subheader("📌 Recommendations")

    st.markdown("""
    ### 1. Prioritize re-engagement of inactive customers

    Develop targeted re-engagement campaigns for inactive customers,
    particularly those aged 46–65. Monitor changes in customer activity
    before and after intervention.
    """)

    st.markdown("""
    ### 2. Strengthen early customer onboarding

    Investigate the customer journey during the first year of the
    relationship, particularly for customers showing early signs of
    disengagement.
    """)

    st.markdown("""
    ### 3. Develop Germany-specific retention strategies

    Investigate why churn is substantially higher in Germany. Areas for
    further investigation could include customer experience, pricing,
    product usage, competition, and service quality.
    """)

    st.markdown("""
    ### 4. Investigate customers with multiple products

    The unusually high churn among customers with 3–4 products warrants
    further investigation. Because these groups are small, additional data
    should be examined before designing a specific intervention around this
    finding.
    """)

    st.markdown("""
    ### 5. Use targeted rather than blanket retention strategies

    Focus retention resources on customers displaying multiple risk signals,
    such as **older age + inactivity + high-risk geography**, rather than
    treating all customers as equally likely to churn.
    """)

    st.markdown("""
    ### 6. Monitor weak predictors carefully

    Variables such as estimated salary and credit-card ownership currently
    show limited separation in churn. These factors should therefore receive
    lower priority in retention decisions unless additional analysis reveals
    stronger relationships.
    """)

    st.info("""
        **Customer churn appears to be concentrated among specific customer 
        segments rather than being evenly distributed across the customer base. 
        Older, inactive customers—particularly those in Germany—represent some of 
        the clearest high-risk groups, while engagement and tenure appear to be important areas for retention efforts.**
    """)
