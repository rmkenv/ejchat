import pandas as pd
import streamlit as st
import io

# Function to load data
@st.cache
def load_data(url):
    return pd.read_csv(url)

# Load the main dataset and the details dataset
df = load_data("https://github.com/rmkenv/ejchat/blob/main/ejtoolmatrix.csv?raw=true")
df_details = load_data("https://raw.githubusercontent.com/rmkenv/ejchat/main/demographics")

# Process and store tool indicators
tool_indicators = {}
for i in range(2, len(df), 2):  # Start from the third row, skipping 'Metric' and 'Source'
    tool_name = df.iloc[i]['Unnamed: 0'].split(' - ')[0]
    indicators = set()
    for col in df.columns[1:]:
        indicator = df.iloc[i][col]
        if pd.notna(indicator):
            indicators.add(indicator)
    tool_indicators[tool_name] = indicators

# Function to compare tool indicators
def compare_tool_indicators(tool1, tool2, tool3):
    indicators_tool1 = tool_indicators[tool1]
    indicators_tool2 = tool_indicators[tool2]
    indicators_tool3 = tool_indicators[tool3] if tool3 != "None" else set()

    # Find unique and common indicators
    unique_to_tool1 = indicators_tool1 - indicators_tool2 - indicators_tool3
    unique_to_tool2 = indicators_tool2 - indicators_tool1 - indicators_tool3
    unique_to_tool3 = indicators_tool3 - indicators_tool1 - indicators_tool2 if tool3 != "None" else set()
    common_to_all = indicators_tool1 & indicators_tool2 & (indicators_tool3 if tool3 != "None" else indicators_tool1)

    return unique_to_tool1, unique_to_tool2, unique_to_tool3, common_to_all

# New function to aggregate demographic differences
def aggregate_demographics(indicators, tool_name):
    demographics = {
        "Tool": [],
        "Indicator": [],
        "Demographic Details": []
    }
    for indicator in indicators:
        demographics["Tool"].append(tool_name)
        demographics["Indicator"].append(indicator)

        # Lookup demographic details
        details = df_details[df_details["Indicator"] == indicator]
        if not details.empty:
            demographics["Demographic Details"].append(details["Demographic Info"].values[0])
        else:
            demographics["Demographic Details"].append("No Details Available")
    return demographics

# Streamlit app setup
st.title("Environmental Tools Indicator Comparison")

# Dropdowns for tool selection
tool1 = st.selectbox("Select the first tool:", list(tool_indicators.keys()), index=0)
tool2 = st.selectbox("Select the second tool:", list(tool_indicators.keys()), index=1)
tool3 = st.selectbox("Select the third tool (optional):", ["None"] + list(tool_indicators.keys()), index=0)

# Button to compare tools
if st.button("Compare Tools"):
    unique_to_tool1, unique_to_tool2, unique_to_tool3, common_to_all = compare_tool_indicators(tool1, tool2, tool3)

    # Prepare a DataFrame for displaying results
    results = {
        "Indicator": [],
        "Unique to": []
    }

    # Function to add details to the results
    def add_details(indicators, tool_name):
        for indicator in indicators:
            results["Indicator"].append(indicator)
            results["Unique to"].append(tool_name)

    # Add data to the results DataFrame
    add_details(unique_to_tool1, tool1)
    add_details(unique_to_tool2, tool2)
    if tool3 != "None":
        add_details(unique_to_tool3, tool3)
    if common_to_all:
        add_details(common_to_all, "Common to All")

    # Convert results to DataFrame and display
    results_df = pd.DataFrame(results)
    st.subheader("Indicator Differences")
    st.dataframe(results_df)

    # Preparing the second table for demographic differences
    demo_results = {
        "Tool": [],
        "Indicator": [],
        "Demographic Details": []
    }

    # Aggregate demographic information
    for tool, indicators in [(tool1, unique_to_tool1), (tool2, unique_to_tool2), (tool3, unique_to_tool3 if tool3 != "None" else set()), ("Common to All", common_to_all)]:
        demo_info = aggregate_demographics(indicators, tool)
        demo_results["Tool"].extend(demo_info["Tool"])
        demo_results["Indicator"].extend(demo_info["Indicator"])
        demo_results["Demographic Details"].extend(demo_info["Demographic Details"])

    # Convert demographic results to DataFrame and display
    demo_results_df = pd.DataFrame(demo_results)
    st.subheader("Demographic Differences")
    st.dataframe(demo_results_df)

    # Allow downloading as CSV
    csv = results_df.to_csv(index=False)
    b = io.BytesIO(csv.encode())
    st.download_button(label="Download comparison results as CSV", data=b, file_name='comparison_results.csv', mime='text/csv')

    # Allow downloading demographic results as CSV
    csv_demo = demo_results_df.to_csv(index=False)
    b_demo = io.BytesIO(csv_demo.encode())
    st.download_button(label="Download demographic comparison results as CSV", data=b_demo, file_name='demographic_comparison_results.csv', mime='text/csv')
