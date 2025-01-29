import pandas as pd
from taipy.gui import Gui, notify
import taipy.gui.builder as tgb

# Load data
data = pd.read_excel("supermarket_sales.xlsx")

# Add 'hour' column to dataframe
data["hour"] = pd.to_datetime(data["Time"], format="%H:%M:%S").dt.hour

# Prepare filter options
cities = list(data["City"].unique())
selected_cities = cities  # Multi-select enabled

customer_types = list(data["Customer_type"].unique())
selected_customer_types = customer_types  # Multi-select enabled

genders = list(data["Gender"].unique())
selected_genders = genders  # Multi-select enabled

# Initialize state variables
Total_Sales = data["Total"].sum()
Average_Sales = data["Total"].mean()
Total_Customers = len(data["Invoice ID"].unique())
filtered_data = data

chart_data_gender = (
    data.groupby("Gender")["Total"]
    .sum()
    .sort_values(ascending=False)
    .reset_index())
chart_data_hour = (
    data.groupby("hour")["Total"]
    .sum()
    .reset_index())
chart_data_product = (
    data.groupby("Product line")["Total"]
    .sum()
    .reset_index())
chart_data_payment = (
    data.groupby("Payment")["Total"]
    .sum()
    .reset_index())

# Filter function
def on_filter(state):
    filtered_data = data[
        data["City"].isin(state.selected_cities) &
        data["Customer_type"].isin(state.selected_customer_types) &
        data["Gender"].isin(state.selected_genders)
    ]
    state.Total_Sales = filtered_data["Total"].sum()
    state.Average_Sales = filtered_data["Total"].mean()
    state.Total_Customers = len(filtered_data["Invoice ID"].unique())
    
    # Update charts
    state.chart_data_gender = (
        filtered_data.groupby("Gender")["Total"]
        .sum()
        .sort_values(ascending=False)
        .reset_index())
    state.chart_data_hour = (
        filtered_data.groupby("hour")["Total"]
        .sum()
        .reset_index())
    state.chart_data_product = (
        filtered_data.groupby("Product line")["Total"]
        .sum()
        .reset_index())
    state.chart_data_payment = (
        filtered_data.groupby("Payment")["Total"]
        .sum()
        .reset_index())
    state.filtered_data = filtered_data

# GUI Layout
with tgb.Page() as page1:
    tgb.toggle(theme=True)
    tgb.text("#  🛒Supermarket Sales Dashboard", mode="md", class_name="text-center")
    # Summary Cards
    with tgb.layout("1 1 1", class_name="p1"):
        with tgb.part(class_name="card"):
            tgb.text("## 📊 Total Sales", mode="md")
            tgb.text("US $ {Total_Sales:.2f}", class_name="h4")
        with tgb.part(class_name="card"):
            tgb.text("## 💰 Average Sales", mode="md")
            tgb.text("US $ {Average_Sales:.2f}", class_name="h4")
        with tgb.part(class_name="card"):
            tgb.text("## 👥 Total Customers", mode="md")
            tgb.text("{Total_Customers}", class_name="h4")
    
    # Filters and Apply Button
    with tgb.layout("1 1 1 1", class_name="p1"):
        
        tgb.selector(
            value="{selected_cities}",
            lov=cities,
            dropdown=True,
            label="Select Cities")
        tgb.selector(
            value="{selected_customer_types}",
            lov=customer_types,
            dropdown=True,
            multiple=True,
            label="Select Customer Types")
        tgb.selector(
            value="{selected_genders}",
            lov=genders,
            dropdown=True,
            multiple=True,
            label="Select Genders")
        # Apply Button
        tgb.button("Apply", on_action=on_filter, class_name="primary fullwidth")
    
    # Charts Section
    tgb.text("# Sales by Gender and hour", mode="md",class_name="text-center")
    with tgb.layout("1 1", class_name="p1"):
        tgb.chart(
            data="{chart_data_gender}",
            type="bar",
            x="Gender",
            y="Total",
            title="Sales by Gender",on_action=on_filter)
        tgb.chart(
            data="{chart_data_hour}",
            type="line",
            x="hour",
            y="Total",
            title="Sales by Hour",on_action=on_filter)
    
    # Page 2: Sales Insights
with tgb.Page() as page2:
    tgb.text("# 📈 Sales Insights", mode="md", class_name="text-center")
    with tgb.layout("1 1", class_name="p1"):
        tgb.chart(
            data="{chart_data_product}",
            type="pie",
            values="Total",
            labels="Product line",
            title="Sales Distribution by Product",on_action=on_filter)
        tgb.table(data="{chart_data_product}")
        tgb.chart(
            data="{chart_data_payment}",
            type="bar",
            x="Payment",
            y="Total",
            title="Sales by Payment Mode",on_action=on_filter)
        tgb.table(data="{chart_data_payment}")
        
    # Filtered Data Table
with tgb.Page() as page3:
    with tgb.expandable("📄 Data Table",mode="md", class_name="text-center"):
        tgb.table(data="{filtered_data}",on_action=on_filter)

with tgb.Page() as root_page:
    tgb.navbar()

# Define pages dictionary
pages = {
    "/": root_page,
    "Overview":  page1,
    "Sales_Insight":page2,
    "Data":page3}

# Run the app
app = Gui(pages=pages)
app.run(
    use_reloader=True,
    title="Supermarket Dashboard ",
    dark_mode=False,
    stylekit={"color-primary": "#007bff", "font-family": "Georgia,serif"})
