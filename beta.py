import streamlit as st
import pandas as pd

# Load the data from GitHub
@st.cache
def load_data():
    url = 'https://raw.githubusercontent.com/rmkenv/ejchat/main/ejmatrix_cleaned.csv'
    data = pd.read_csv(url)
    return data

df = load_data()

# Select Tools
tool_options = df['tool name'].unique()
selected_tools = st.multiselect('Select up to 3 tools to compare:', tool_options, default=tool_options[:3])

# Filter data based on selection
if selected_tools:
    filtered_df = df[df['tool name'].isin(selected_tools)]

    # Assuming that the DataFrame 'filtered_df' now contains the rows for the selected tools,
    # and each column (other than 'tool name' and maybe 'Affilation') represents a different indicator.
    # We need to highlight differences between the tools. This can be a complex task depending on the data's nature.
    # A simple way could be to transpose the data for better visualization.
    comparison_df = filtered_df.set_index('tool name').T

    st.dataframe(comparison_df.style.apply(lambda x: ["background: yellow" if v != x[0] else "" for v in x], axis=1))

# Instructions for running the Streamlit app
# Save this script as app.py and run it using the command: streamlit run app.py

# Title for the Streamlit app
st.title("Environmental Justice Datasets Comparison App")

# Text description box
st.markdown("EJ Data is different depending on the state and federal level. This tool aims to simplify the comparisons of EJ indicators and data sources for up to 3 tools. The data is derived from the work of Konisky, D., Gonzalez, D., & Leatherman, K. (2021). Mapping for Environmental Justice: An Analysis of State Level Tools. Indiana University’s Paul H. O’Neill School of Public and Environmental Affairs and Environmental Resilience Institute. [Link to the dataset](https://hdl.handle.net/2022/29445)")

# Custom HTML
# Using Markdown to create a hyperlink
st.markdown("[Buy me a coffee ☕](https://www.buymeacoffee.com/kmetzrm)", unsafe_allow_html=True)

fork_on_github_style = """
<style>
#forkongithub a {
    background: #ff6700;
    color: #fff;
    text-decoration: none;
    font-family: arial, sans-serif;
    text-align: center;
    font-weight: bold;
    padding: 5px 40px;
    font-size: 1rem;
    line-height: 2rem;
    position: relative;
    transition: 0.5s;
}
#forkongithub a:hover {
    background: #c11;
    color: #fff;
}
#forkongithub a::before, #forkongithub a::after {
    content: "";
    width: 100%;
    display: block;
    position: absolute;
    top: 1px;
    left: 0;
    height: 1px;
    background: #fff;
}
#forkongithub a::after {
    bottom: 1px;
    top: auto;
}
@media screen and (min-width:800px) {
    #forkongithub {
        position: fixed;
        display: block;
        top: 0;
        right: 0;
        width: 200px;
        overflow: hidden;
        height: 200px;
        z-index: 9999;
    }
    #forkongithub a {
        width: 200px;
        position: absolute;
        top: 60px;
        right: -60px;
        transform: rotate(45deg);
        -webkit-transform: rotate(45deg);
        -ms-transform: rotate(45deg);
        -moz-transform: rotate(45deg);
        -o-transform: rotate(45deg);
        box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.8);
    }
}
</style>
<span id="forkongithub"><a href="https://github.com/rmkenv/ejchat/tree/main">Fork me on GitHub</a></span>
"""

# Use Markdown to render HTML/JS
st.markdown(buy_me_coffee_script, unsafe_allow_html=True)
st.markdown(fork_on_github_style, unsafe_allow_html=True)

