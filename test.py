import streamlit as st
import json
from openai import OpenAI

st.header('LLM with Gaphor')
user_input = st.text_input(label='Enter Your Description below:', placeholder="Type something...")
client = OpenAI(api_key="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", base_url="https://api.perplexity.ai")

if st.button('Generate JSON'):
    try:
        # Construct the messages list
        messages = [
            {"role": "system", "content": "You are a helpful assistant that generates valid JSON structures based on the user's input. Respond with only the JSON."},
            {"role": "user", "content": user_input}
        ]

        # Call OpenAI API with the correct format
        response = client.chat.completions.create(
            model="llama-3.1-sonar-large-128k-online",  # Replace with your model
            messages=messages
        )

        # Extract the content
        raw_output = response.choices[0].message.content.strip()

        # Remove any text before or after the JSON
        start_index = raw_output.find("{")
        end_index = raw_output.rfind("}")
        if start_index != -1 and end_index != -1:
            json_string = raw_output[start_index:end_index + 1]
        else:
            raise ValueError("No valid JSON found in the response.")

        # Parse and display JSON
        try:
            generated_json = json.loads(json_string)  # Parse the JSON
            st.write("### Generated JSON:")
            st.json(generated_json)
        except json.JSONDecodeError:
            st.error("The extracted content is not valid JSON. Here is the raw output:")
            st.code(raw_output)

    except Exception as e:
        st.error(f"An error occurred: {e}")
