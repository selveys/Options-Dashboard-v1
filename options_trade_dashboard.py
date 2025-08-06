import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Options Trade Evaluator", layout="wide")
st.title("📊 Options Trade Evaluator Dashboard")

# --- Ticker Input ---
st.sidebar.header("Live Market Data")
ticker = st.sidebar.text_input("Enter Ticker Symbol", value="AAPL")

if ticker:
    stock = yf.Ticker(ticker)
    try:
        current_price = stock.history(period="1d")['Close'][-1]
        st.sidebar.metric("Current Stock Price", f"${current_price:.2f}")

        expirations = stock.options
        selected_date = st.sidebar.selectbox("Select Expiration Date", expirations)

        if selected_date:
            options_chain = stock.option_chain(selected_date)
            option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])
            df = options_chain.calls if option_type == "Call" else options_chain.puts

            # Filter strikes near current price
            df_filtered = df[(df['strike'] >= current_price * 0.8) & (df['strike'] <= current_price * 1.2)]
            selected_strike = st.sidebar.selectbox("Select Strike Price", df_filtered['strike'].tolist())

            selected_row = df_filtered[df_filtered['strike'] == selected_strike].iloc[0]
            premium = (selected_row['bid'] + selected_row['ask']) / 2

            contracts = st.sidebar.number_input("Number of Contracts", value=1, step=1)

            # --- P&L Calculation ---
            contract_multiplier = 100
            x = np.linspace(current_price * 0.5, current_price * 1.5, 200)

            if option_type == "Call":
                profit = np.maximum(x - selected_strike, 0) - premium
                breakeven = selected_strike + premium
                max_profit = "Unlimited"
            else:
                profit = np.maximum(selected_strike - x, 0) - premium
                breakeven = selected_strike - premium
                max_profit = f"${premium * contracts * contract_multiplier:.2f}"

            total_profit = profit * contracts * contract_multiplier

            # --- Outputs ---
            st.subheader("Trade Summary")
            st.markdown(f"**Option Type:** {option_type}")
            st.markdown(f"**Strike Price:** ${selected_strike:.2f}")
            st.markdown(f"**Premium (Midpoint of Bid/Ask):** ${premium:.2f}")
            st.markdown(f"**Expiration:** {selected_date}")
            st.markdown(f"**Breakeven Price:** ${breakeven:.2f}")

            # --- Chart ---
            st.subheader("Profit / Loss at Expiration")
            fig, ax = plt.subplots()
            ax.plot(x, total_profit, label="P&L", linewidth=2)
            ax.axhline(0, color="gray", linestyle="--")
            ax.axvline(current_price, color="blue", linestyle=":", label="Current Price")
            ax.set_xlabel("Stock Price at Expiration ($)")
            ax.set_ylabel("Profit / Loss ($)")
            ax.set_title("Options P&L at Expiration")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

            # --- Final Metrics ---
            st.metric("Max Profit", max_profit)
            st.metric("Max Loss", f"${premium * contracts * contract_multiplier:.2f}")

            # --- Optional: Full Options Table ---
            with st.expander("View Full Options Chain"):
                st.subheader("Calls")
                st.dataframe(options_chain.calls)
                st.subheader("Puts")
                st.dataframe(options_chain.puts)

    except Exception as e:
        st.error(f"Error retrieving data for ticker '{ticker}': {e}")

