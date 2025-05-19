import streamlit as st
import pandas as pd
import numpy as np

def calculate_loan_basic(principal, rate, time):
    interest = (principal * rate * time) / 100
    total = principal + interest
    emi = total / (time * 12)
    return interest, total, emi

def calculate_loan_advanced(principal, rate, time, processing_fee_percent=1):
    processing_fee = (principal * processing_fee_percent) / 100
    monthly_rate = rate / (12 * 100)
    emi = principal * monthly_rate * (1 + monthly_rate)**(time*12) / ((1 + monthly_rate)**(time*12) - 1)
    total_payment = emi * time * 12
    total_interest = total_payment - principal
    return emi, total_payment, total_interest, processing_fee

def calculate_fd(principal, rate, time, payout_frequency=12):
    if payout_frequency == 0:  # For cumulative
        amount = principal * (1 + rate/100)**(time)
        interest = amount - principal
    else:  # For non-cumulative
        interest = (principal * rate * time) / 100
        amount = principal + interest
    return amount, interest

def calculate_rd(monthly_deposit, rate, time):
    months = time * 12
    total_deposit = monthly_deposit * months
    amount = monthly_deposit * ((1 + rate/1200)**months - 1) * (1 + rate/1200)/(rate/1200)
    interest = amount - total_deposit
    return amount, interest, total_deposit

def calculate_ppf(yearly_deposit, time):
    rate = 7.1  # Current PPF rate
    amount = 0
    for i in range(time):
        amount = (amount + yearly_deposit) * (1 + rate/100)
    interest = amount - (yearly_deposit * time)
    return amount, interest

def calculate_sip(monthly_investment, expected_return, time_years):
    monthly_rate = expected_return / (12 * 100)
    months = time_years * 12
    
    # Calculate future value using SIP formula
    future_value = monthly_investment * ((1 + monthly_rate) * ((1 + monthly_rate)**months - 1) / monthly_rate)
    
    total_investment = monthly_investment * months
    total_returns = future_value - total_investment
    
    return future_value, total_investment, total_returns

def main():
    st.title("Financial Calculator Hub")
    
    calculator_type = st.sidebar.selectbox(
        "Select Calculator Type",
        ["Loan - Basic", "Loan - Advanced", "Fixed Deposit", "Recurring Deposit",
         "PPF", "Sukanya Samriddhi", "Senior Citizens Savings", "Kisan Vikas Patra",
         "Monthly Income Scheme", "National Savings Certificate", "SIP Calculator"]
    )
    
    if calculator_type == "Loan - Basic":
        st.header("Basic Loan Calculator")
        principal = st.number_input("Principal Amount (₹)", min_value=1000)
        rate = st.number_input("Interest Rate (%)", min_value=1.0)
        time = st.number_input("Time Period (Years)", min_value=1)
        
        if st.button("Calculate"):
            interest, total, emi = calculate_loan_basic(principal, rate, time)
            st.write(f"Monthly EMI: ₹{emi:.2f}")
            st.write(f"Total Interest: ₹{interest:.2f}")
            st.write(f"Total Amount: ₹{total:.2f}")
    
    elif calculator_type == "Loan - Advanced":
        st.header("Advanced Loan Calculator")
        principal = st.number_input("Principal Amount (₹)", min_value=1000)
        rate = st.number_input("Interest Rate (%)", min_value=1.0)
        time = st.number_input("Time Period (Years)", min_value=1)
        processing_fee = st.number_input("Processing Fee (%)", min_value=0.0)
        
        if st.button("Calculate"):
            emi, total, interest, proc_fee = calculate_loan_advanced(principal, rate, time, processing_fee)
            st.write(f"Monthly EMI: ₹{emi:.2f}")
            st.write(f"Total Interest: ₹{interest:.2f}")
            st.write(f"Processing Fee: ₹{proc_fee:.2f}")
            st.write(f"Total Amount: ₹{total:.2f}")
    
    elif calculator_type == "Fixed Deposit":
        st.header("Fixed Deposit Calculator")
        fd_type = st.selectbox("Select FD Type", ["Cumulative (STDR)", "Non-Cumulative (TDR)"])
        principal = st.number_input("Principal Amount (₹)", min_value=1000)
        rate = st.number_input("Interest Rate (%)", min_value=1.0)
        time = st.number_input("Time Period (Years)", min_value=1)
        
        if st.button("Calculate"):
            payout_freq = 0 if fd_type == "Cumulative (STDR)" else 12
            amount, interest = calculate_fd(principal, rate, time, payout_freq)
            st.write(f"Maturity Amount: ₹{amount:.2f}")
            st.write(f"Total Interest: ₹{interest:.2f}")
    
    elif calculator_type == "Recurring Deposit":
        st.header("Recurring Deposit Calculator")
        monthly_deposit = st.number_input("Monthly Deposit (₹)", min_value=100)
        rate = st.number_input("Interest Rate (%)", min_value=1.0)
        time = st.number_input("Time Period (Years)", min_value=1)
        
        if st.button("Calculate"):
            amount, interest, total_deposit = calculate_rd(monthly_deposit, rate, time)
            st.write(f"Maturity Amount: ₹{amount:.2f}")
            st.write(f"Total Interest: ₹{interest:.2f}")
            st.write(f"Total Deposit: ₹{total_deposit:.2f}")
    
    elif calculator_type == "PPF":
        st.header("Public Provident Fund Calculator")
        yearly_deposit = st.number_input("Yearly Deposit (₹)", min_value=500, max_value=150000)
        time = st.number_input("Time Period (Years)", min_value=15, max_value=50)
        
        if st.button("Calculate"):
            amount, interest = calculate_ppf(yearly_deposit, time)
            st.write(f"Maturity Amount: ₹{amount:.2f}")
            st.write(f"Total Interest: ₹{interest:.2f}")
            st.write(f"Total Deposit: ₹{yearly_deposit * time:.2f}")

    elif calculator_type == "SIP Calculator":
        st.header("SIP (Systematic Investment Plan) Calculator")
        monthly_investment = st.number_input("Monthly Investment Amount (₹)", min_value=100)
        expected_return = st.number_input("Expected Annual Return (%)", min_value=1.0, value=12.0)
        time_years = st.number_input("Investment Period (Years)", min_value=1)
        
        if st.button("Calculate"):
            future_value, total_investment, total_returns = calculate_sip(monthly_investment, expected_return, time_years)
            
            st.write(f"Future Value: ₹{future_value:,.2f}")
            st.write(f"Total Investment: ₹{total_investment:,.2f}")
            st.write(f"Total Returns: ₹{total_returns:,.2f}")
            
            # Create a breakdown of investment vs returns
            data = {
                'Component': ['Total Investment', 'Total Returns'],
                'Amount': [total_investment, total_returns]
            }
            df = pd.DataFrame(data)
            st.bar_chart(df.set_index('Component'))
            
            # Monthly investment table
            years = list(range(1, time_years + 1))
            yearly_data = []
            
            for year in years:
                fv, inv, ret = calculate_sip(monthly_investment, expected_return, year)
                yearly_data.append({
                    'Year': year,
                    'Investment': inv,
                    'Returns': ret,
                    'Total Value': fv
                })
            
            st.subheader("Year-wise Breakdown")
            yearly_df = pd.DataFrame(yearly_data)
            st.dataframe(yearly_df.style.format({
                'Investment': '₹{:,.2f}',
                'Returns': '₹{:,.2f}',
                'Total Value': '₹{:,.2f}'
            }))

    # Add similar sections for other calculators...

if __name__ == "__main__":
    main()
