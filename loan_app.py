import streamlit as st
import math
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Loan Calculator", layout="centered")
st.title(" Loan Calculator")

# Inputs
loan_amount = st.number_input("Loan Amount (₹)", min_value=1000, step=1000, value=100000)
interest_rate = st.number_input("Annual Interest Rate (%)", min_value=1.0, step=0.1, value=10.0)
loan_years = st.number_input("Loan Term (Years)", min_value=1, step=1, value=5)

# EMI Calculation
monthly_rate = interest_rate / 100 / 12
num_payments = loan_years * 12

if monthly_rate > 0:
    emi = loan_amount * monthly_rate * (1 + monthly_rate) ** num_payments / ((1 + monthly_rate) ** num_payments - 1)
else:
    emi = loan_amount / num_payments

total_payment = emi * num_payments
total_interest = total_payment - loan_amount

# 📊 Loan Summary
st.subheader("📌 Loan Summary")
summary_df = pd.DataFrame({
    "Details": ["Loan Amount", "Monthly EMI", "Total Interest", "Total Payment"],
    "Amount (₹)": [loan_amount, round(emi, 2), round(total_interest, 2), round(total_payment, 2)]
})
st.table(summary_df)

# 📆 Amortization Schedule (Yearly)
st.subheader("📆 Amortization Schedule (Yearly)")
balance = loan_amount
schedule = []

for year in range(1, loan_years + 1):
    interest_paid = 0
    principal_paid = 0
    for m in range(12):
        interest_component = balance * monthly_rate
        principal_component = emi - interest_component
        balance -= principal_component
        interest_paid += interest_component
        principal_paid += principal_component
    schedule.append([year, round(principal_paid, 2), round(interest_paid, 2), round(balance if balance > 0 else 0, 2)])

schedule_df = pd.DataFrame(schedule, columns=["Year", "Principal Paid (₹)", "Interest Paid (₹)", "Balance (₹)"])
st.dataframe(schedule_df)

# 📊 Pie Chart
st.subheader("📊 Payment Distribution")
labels = ['Principal', 'Interest']
sizes = [loan_amount, total_interest]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# 📊 Bar Chart (Yearly Breakdown)
st.subheader("📊 Yearly Principal vs Interest")
fig2, ax2 = plt.subplots()
ax2.bar(schedule_df["Year"], schedule_df["Principal Paid (₹)"], label="Principal")
ax2.bar(schedule_df["Year"], schedule_df["Interest Paid (₹)"], bottom=schedule_df["Principal Paid (₹)"], label="Interest")
ax2.set_xlabel("Year")
ax2.set_ylabel("Amount (₹)")
ax2.legend()
st.pyplot(fig2)

