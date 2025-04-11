import streamlit as st
import json
from pathlib import Path
from xmltodict import unparse  # For converting JSON to XML
from openai import OpenAI

st.header("LLM with Gaphor")
user_input = st.text_input(label="Enter Your Description below:", placeholder="Type something...")
client = OpenAI(api_key="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", base_url="https://api.perplexity.ai")
json_file_path = "Requirements.json"

# Step 1: Generate JSON
if st.button("Generate JSON"):
    try:
        # Simulating the response from the OpenAI API
        with open(json_file_path, "r") as file:
            generated_json = json.load(file)
    
        # Display generated JSON
        st.write("### Generated JSON:")
        st.json(generated_json)

        # Save JSON for the next step
        st.session_state["generated_json"] = generated_json
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Step 2: Generate Gaphor Model
if "generated_json" in st.session_state and st.button("Generate Gaphor XML"):
    try:
        json_data = st.session_state["generated_json"]

        # Convert JSON to .gaphor-compatible XML
        gaphor_xml = unparse(json_data, pretty=True)

        # Save the XML content to a file
        gaphor_file_path = "generated_model.gaphor"
        with open(gaphor_file_path, "w", encoding="utf-8") as file:
            file.write(gaphor_xml)

        st.write("Generated Gaphor XML:")
        st.code(gaphor_xml)

        # Provide download button
        with open(gaphor_file_path, "rb") as file:
            st.download_button(
                label="Download Gaphor Model",
                data=file.read(),
                file_name="generated_model.gaphor",
                mime="application/octet-stream",
            )

    except Exception as e:
        st.error("An error occurred while generating the Gaphor XML.")
        st.error(str(e))