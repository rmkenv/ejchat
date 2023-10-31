import pandas as pd
import streamlit as st
import io

# Load the datasets from URLs or files
@st.cache
def load_data(url):
    return pd.read_csv(url)

# Replace these URLs with the actual paths or URLs of your datasets
df = load_data("https://github.com/rmkenv/ejchat/blob/main/ejtoolmatrix.csv?raw=true")
df_details = load_data("https://github.com/rmkenv/ejchat/blob/main/demographics")

# Process the first dataframe to get tool names and indicators
tool_indicators = {}
for i in range(2, len(df), 2):
    tool_name = df.iloc[i]['Unnamed: 0'].split(' - ')[0]
    indicators = set()
    for col in df.columns[1:]:
        indicator = df.iloc[i][col]
        if pd.notna(indicator):
            indicators.add(indicator)
    tool_indicators[tool_name] = indicators

# Function to get detailed information for indicators
def get_indicator_details(indicators):
    details = {}
    for indicator in indicators:
        detail_rows = df_details[df_details['Indicator'].isin([indicator])]
        if not detail_rows.empty:
            details[indicator] = detail_rows.to_dict('records')[0]  # Get the first matching record as a dictionary
    return details

# Updated function to compare tool indicators
def compare_tool_indicators(tool1, tool2, tool3):
    indicators_tool1 = tool_indicators[tool1]
    indicators_tool2 = tool_indicators[tool2]
    indicators_tool3 = tool_indicators[tool3] if tool3 != "None" else set()

    # Find unique and common indicators
    unique_to_tool1 = indicators_tool1 - indicators_tool2 - indicators_tool3
    unique_to_tool2 = indicators_tool2 - indicators_tool1 - indicators_tool3
    unique_to_tool3 = indicators_tool3 - indicators_tool1 - indicators_tool2 if tool3 != "None" else set()
    common_to_all = indicators_tool1 & indicators_tool2 & (indicators_tool3 if tool3 != "None" else indicators_tool1)

    # Now get details for these indicators
    details_tool1 = get_indicator_details(unique_to_tool1)
    details_tool2 = get_indicator_details(unique_to_tool2)
    details_tool3 = get_indicator_details(unique_to_tool3) if tool3 != "None" else {}
    common_details = get_indicator_details(common_to_all)

    return unique_to_tool1, unique_to_tool2, unique_to_tool3, common_to_all, details_tool1, details_tool2, details_tool3, common_details

# Streamlit app UI
st.title("Environmental Tools Indicator Comparison")

# Dropdown for selecting tools
tool_list = list(tool_indicators.keys())
tool1 = st.selectbox("Select the first tool:", tool_list, index=0)
tool2 = st.selectbox("Select the second tool:", tool_list, index=1)
tool3 = st.selectbox("Select the third tool (optional):", ["None"] + tool_list, index=0)

# Button to compare indicators
if st.button("Compare Tools"):
    unique_to_tool1, unique_to_tool2, unique_to_tool3, common_to_all, details_tool1, details_tool2, details_tool3, common_details = compare_tool_indicators(tool1, tool2, tool3)

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

    # Prepare the data for CSV download
    def prepare_data_for_download(details, tool_name):
        return [[tool_name, indicator, detail.get('Category', ''), detail.get('Metric', '')] for indicator, detail in details.items()]

    # Aggregate data for all tools
    all_data = []
    all_data.extend(prepare_data_for_download(details_tool1, tool1))
    all_data.extend(prepare_data_for_download(details_tool2, tool2))
    if tool3 != "None":
        all_data.extend(prepare_data_for_download(details_tool3, tool3))
    all_data.extend(prepare_data_for_download(common_details, "Common"))

    # Convert to DataFrame and download
    results_df = pd.DataFrame(all_data, columns=["Tool", "Indicator", "Category", "Metric"])
    
    # Allow downloading as CSV
    csv = results_df.to_csv(index=False)
    b = io.BytesIO(csv.encode())
    st.download_button(label="Download comparison results as CSV", data=b, file_name='comparison_results.csv', mime='text/csv')
