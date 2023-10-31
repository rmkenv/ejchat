import pandas as pd
import streamlit as st
import io

# Load the dataset from the provided GitHub URL
@st.cache
def load_data(url):
    data = pd.read_csv(url)
    return data

df = load_data("https://github.com/rmkenv/ejchat/blob/main/ejtoolmatrix.csv?raw=true")

# Dictionary to hold tool names and their indicators
tool_indicators = {}

# Process the dataframe
for i in range(2, len(df), 2):  # Start from the third row, skipping 'Metric' and 'Source'
    tool_name = df.iloc[i]['Unnamed: 0'].split(' - ')[0]
    indicators = set()
    for col in df.columns[1:]:
        indicator = df.iloc[i][col]
        if pd.notna(indicator):
            indicators.add(indicator)
    tool_indicators[tool_name] = indicators

def compare_tool_indicators(tool1, tool2, tool3):
    """Function to compare indicators among up to three tools."""
    indicators_tool1 = tool_indicators[tool1]
    indicators_tool2 = tool_indicators[tool2]
    indicators_tool3 = tool_indicators[tool3] if tool3 != "None" else set()

    # Find unique and common indicators
    unique_to_tool1 = indicators_tool1 - indicators_tool2 - indicators_tool3
    unique_to_tool2 = indicators_tool2 - indicators_tool1 - indicators_tool3
    unique_to_tool3 = indicators_tool3 - indicators_tool1 - indicators_tool2 if tool3 != "None" else set()
    common_to_all = indicators_tool1 & indicators_tool2 & (indicators_tool3 if tool3 != "None" else indicators_tool1)

    return unique_to_tool1, unique_to_tool2, unique_to_tool3, common_to_all

# Streamlit app
st.title("Environmental Tools Indicator Comparison")

# Dropdown for selecting tools
tool_list = list(tool_indicators.keys())
tool1 = st.selectbox("Select the first tool:", tool_list, index=0)
tool2 = st.selectbox("Select the second tool:", tool_list, index=1)
tool3 = st.selectbox("Select the third tool (optional):", ["None"] + tool_list, index=0)

# Button to compare indicators
if st.button("Compare Tools"):
    unique_to_tool1, unique_to_tool2, unique_to_tool3, common_to_all = compare_tool_indicators(tool1, tool2, tool3)

    # Display results
    st.write(f"Indicators unique to {tool1}:")
    st.write(unique_to_tool1)
    st.write(f"Indicators unique to {tool2}:")
    st.write(unique_to_tool2)
    if tool3 != "None":
        st.write(f"Indicators unique to {tool3}:")
        st.write(unique_to_tool3)
    st.write("Indicators common to all selected tools:")
    st.write(common_to_all)

    # Convert results to DataFrame for downloading
    results_dict = {
        tool1: list(unique_to_tool1),
        tool2: list(unique_to_tool2),
        tool3: list(unique_to_tool3) if tool3 != "None" else [],
        "Common": list(common_to_all)
    }
    results_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in results_dict.items()]))
    
    # Allow downloading as CSV
    csv = results_df.to_csv(index=False)
    b = io.BytesIO(csv.encode())
    st.download_button(label="Download comparison results as CSV", data=b, file_name='comparison_results.csv', mime='text/csv')
