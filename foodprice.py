import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title = "🇲🇲 Myanmar Food Prices", layout = "wide")
st.title("🇲🇲 Myanmar Food Prices")

data = pd.read_csv("wfp_food_prices_mmr.csv")
data["date"] = pd.to_datetime(data["date"]) # converting the date to use it again later

st.sidebar.header("🔍 Filter Options")

# to make select commodity, region, currency as default placeholder
commodities = ["Select Commodity"] + data["commodity"].unique().tolist() 
commodity = st.sidebar.selectbox("Commodity", commodities)

regions = ["Select Region"] + data["admin1"].unique().tolist()
region = st.sidebar.selectbox("Region", regions)

currency = st.sidebar.radio("Currency", ["Select Currency", "MMK", "USD"])

if currency == "MMK":
    price_col = "price"
    label = "MMK"
elif currency == "USD":
    price_col = "usdprice"
    label = "USD"
else:
    price_col = None

if commodity != "Select Commodity" and region != "Select Region" and currency != "Select Currency":
    filtered_data = data[(data["commodity"] == commodity) & (data["admin1"] == region)]

    if filtered_data.empty:
        st.info(f"No data found for {commodity} in {region}. Try different combination.")
    else:
        if len(filtered_data) >= 2:
            latest = filtered_data[price_col].iloc[-1] # no need to sort the dates bec dataset is already sorted by date
            previous = filtered_data[price_col].iloc[-2]

            if previous != 0: # to avoid error if the previous price is 0
                change = ((latest - previous) / previous) * 100
            else:
                change = 0

            m1, m2, m3 = st.columns(3)
            m1.metric("Current Price", f"{latest:,.2f} {currency}")
            m2.metric("Previous Price", f"{previous:,.2f} {currency}")
            m3.metric("Percentage Change", f"{change:+.2f}%")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            filtered_data["year"] = filtered_data["date"].dt.year
            year = filtered_data.groupby("year")[price_col].mean()

            st.subheader(f"📈 Yearly Price Trend: {commodity} in {region}")

            fig, ax = plt.subplots()
            ax.plot(year.index, year.values, marker='o', linewidth = 2)
            ax.set_xlabel("Year")
            ax.set_ylabel(f"Average Price ({label})")
            ax.set_title("Yearly Price Trend")
            ax.set_xticks(year.index) # to show all the years without skipping some
            ax.tick_params(axis='x', rotation = 45) # rotates 45 degrees to avoid the labels overlapping each other
            ax.grid(True, linestyle = "-", alpha = 0.5) 
            fig.tight_layout() # prevents labels from getting cut off at the edges

            st.pyplot(fig)

        with col2:
            st.subheader(f"Average Price Across Regions - {commodity}")
            average = data[data["commodity"] == commodity].groupby("admin1")[price_col].mean()
            st.bar_chart(average)

            sorted_average = sorted(average)
            st.metric("Region With Highest Price", f"{average.idxmax()} - {average.max():.2f} {currency}")
            st.metric("Region with Lowest Price", f"{average.idxmin()} - {average.min():.2f} {currency}")

        st.divider()
        st.subheader(f"📍 Market Location - {commodity} in {region}")
        map_data = filtered_data[["latitude", "longitude"]].dropna() # dropna() --> removes rows where latitude or longitude is missing
        st.map(map_data)

        st.divider()
        st.caption("Data sourced from the World Food Programme (WFP)")
else:
    st.warning("Apply all the filters to explore the price trends.")
