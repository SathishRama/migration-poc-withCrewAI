import streamlit as st

st.markdown("# GenAI Assisted C++ to Java Migration Assistant : Guide 🎈")
st.sidebar.markdown("## AI4Tech POC 🎈")

st.markdown("## User Guide")
st.write(
    "Welcome to the C++ to Java Migration Assistant. This guide will help you understand how to use the app effectively.")

st.markdown("### Step-by-Step Instructions:")
st.markdown(
    "1. **Set Target Directory**: Enter a new directory where you want to save the outputs. Click the 'Set Target Directory' button to create the directory.")
st.markdown(
    "2. **Explain the C++ File**: Enter the full path of the C++ file you want to explain. Click the 'Explain the C++ file' button to generate an explanation.")
st.markdown(
    "3. **Save Explanation**: Enter a new file name to save the explanation. Click the 'Save explanation' button to save the explanation as a markdown file in the target directory.")
st.markdown(
    "4. **Convert to Java**: Enter the Java filename you want to create. Click the 'Convert to Java' button to start the migration process. Ensure that you have selected an input file and set the output directory before proceeding.")

st.markdown("### Additional Information:")
st.write("- Ensure that the file paths and directory names are correct to avoid errors.")
st.write("- The status of each task will be displayed on the left side of the app.")
st.write("- If you encounter any issues, please refer to the status messages for more information.")