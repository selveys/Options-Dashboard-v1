import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Options Trade Evaluator", layout="centered")
st.title("📊 Options Trade Evaluator Dashboard")

# --- Inputs ---
st.sidebar.header("Option Parameters")
option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])
stock_price = st.sidebar.number_input("Current Stock Price ($)", value=100.0)
strike_price = st.sidebar.number_input("Strike Price ($)", value=105.0)
premium = st.sidebar.number_input("Premium Paid/Received ($)", value=3.0)
contracts = st.sidebar.number_input("Number of Contracts", value=1, step=1)

# --- Calculations ---
contract_multiplier = 100
x = np.linspace(stock_price * 0.5, stock_price * 1.5, 200)

if option_type == "Call":
    profit = np.maximum(x - strike_price, 0) - premium
else:
    profit = np.maximum(strike_price - x, 0) - premium

total_profit = profit * contracts * contract_multiplier

# --- Outputs ---
st.subheader("Trade Summary")
st.markdown(f"**Option Type:** {option_type}")
st.markdown(f"**Strike Price:** ${strike_price:.2f}")
st.markdown(f"**Premium {'Paid' if premium > 0 else 'Received'}:** ${premium:.2f}")
st.markdown(f"**Breakeven Price:** ${strike_price + premium if option_type == 'Call' else strike_price - premium:.2f}")

# --- Chart ---
st.subheader("Profit / Loss at Expiration")
fig, ax = plt.subplots()
ax.plot(x, total_profit, label="P&L", linewidth=2)
ax.axhline(0, color="gray", linestyle="--")
ax.axvline(stock_price, color="blue", linestyle=":", label="Current Price")
ax.set_xlabel("Stock Price at Expiration ($)")
ax.set_ylabel("Profit / Loss ($)")
ax.set_title("Options P&L at Expiration")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# --- Final Metric ---
st.metric("Max Profit", f"{'Unlimited' if option_type == 'Call' else f'${premium * contracts * contract_multiplier:.2f}'}")
st.metric("Max Loss", f"${premium * contracts * contract_multiplier:.2f}")
