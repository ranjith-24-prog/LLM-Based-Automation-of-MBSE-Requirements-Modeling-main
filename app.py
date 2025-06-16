import streamlit as st
import uuid
import xmltodict
import json
import tempfile
import os
import subprocess
from openai import OpenAI

# Perplexity AI API Key
API_KEY = st.secrets["api_keys"]["perplexity"]

# Constants for Requirement Spacing
MAX_COLUMNS = 3  # Number of requirements per row
X_START = 150    # Starting X coordinate
Y_START = 300    # Starting Y coordinate
X_SPACING = 350  # Horizontal spacing
Y_SPACING = 250  # Vertical spacing

# Function to generate a new UUID
def generate_uuid():
    return str(uuid.uuid4())

# Function to generate the full Gaphor XML structure with correct requirement spacing
def generate_gaphor_xml(headings, descriptions):
    gaphor_structure = {
        "gaphor": {
            "@xmlns": "http://gaphor.sourceforge.net/model",
            "@version": "3.0",
            "@gaphor-version": "2.27.0",
            "StyleSheet": {"@id": generate_uuid()},
            "Package": [
                {
                    "@id": generate_uuid(),
                    "name": {"val": "1. Concept Level"},
                    "nestedPackage": {"reflist": {"ref": {"@refid": generate_uuid()}}}
                },
                {
                    "@id": "012edaba-70f5-11ec-aabc-f47b099bf663",
                    "name": {"val": "Requirements"},
                    "ownedDiagram": {"reflist": {"ref": {"@refid": "01a97fa8-70f6-11ec-aabc-f47b099bf663"}}},
                    "ownedType": {"reflist": {"ref": []}},
                    "package": {"ref": {"@refid": "58d6c2e8-66f8-11ec-b4c8-0456e5e540ed"}}
                }
            ],
            "Diagram": [
                {
                    "@id": "01a97fa8-70f6-11ec-aabc-f47b099bf663",
                    "diagramType": {"val": "req"},
                    "element": {"ref": {"@refid": "012edaba-70f5-11ec-aabc-f47b099bf663"}},
                    "name": {"val": "Concept Requirements"},
                    "ownedPresentation": {"reflist": {"ref": []}},
                    "presentation": {"reflist": {"ref": {"@refid": generate_uuid()}}}
                }
            ],
            "Requirement": [],
            "RequirementItem": []
        }
    }

    for index, (heading, description) in enumerate(zip(headings, descriptions)):
        req_uuid = generate_uuid()
        item_uuid = generate_uuid()

        # Calculate X, Y Position for the Requirement
        row = index // MAX_COLUMNS
        col = index % MAX_COLUMNS
        x_position = X_START + (col * X_SPACING)
        y_position = Y_START + (row * Y_SPACING)

        # Append new requirement
        gaphor_structure["gaphor"]["Requirement"].append({
            "@id": req_uuid,
            "name": {"val": heading},
            "package": {"ref": {"@refid": "012edaba-70f5-11ec-aabc-f47b099bf663"}},
            "presentation": {"reflist": {"ref": {"@refid": item_uuid}}},
            "text": {"val": description}
        })

        # Append new requirement item with proper spacing
        gaphor_structure["gaphor"]["RequirementItem"].append({
            "@id": item_uuid,
            "matrix": {"val": f"(1.0, 0.0, 0.0, 1.0, {x_position}, {y_position})"},
            "top-left": {"val": "(0.0, 0.0)"},
            "width": {"val": "217.0"},
            "height": {"val": "122.0"},
            "diagram": {"ref": {"@refid": "01a97fa8-70f6-11ec-aabc-f47b099bf663"}},
            "subject": {"ref": {"@refid": req_uuid}}
        })

        # Add references to Diagram and Package
        gaphor_structure["gaphor"]["Diagram"][0]["ownedPresentation"]["reflist"]["ref"].append({"@refid": item_uuid})
        gaphor_structure["gaphor"]["Package"][1]["ownedType"]["reflist"]["ref"].append({"@refid": req_uuid})

    return xmltodict.unparse(gaphor_structure, pretty=True)

# Function to generate requirements from Perplexity AI
def generate_requirements_from_llm(prompt, client):
    messages = [
    {
        "role": "system",
        "content": (
            "You are an AI specializing in Model-Based Systems Engineering (MBSE)."
            "Your task is to generate structured, concept-level system requirements in JSON format."
            "Follow best practices from ISO 15288 and MBSE methodologies."
            "Concept-level requirements should focus on high-level needs, core functionality, performance, constraints, and interactions."
            "Avoid detailed technical specifications and implementation details."
            "Ensure requirements align with stakeholder expectations and operational scenarios."

            "\n\n**Key Considerations:**"
            "\n- Identify essential system capabilities."
            "\n- Define high-level constraints (space, power, environment, safety, etc.)."
            "\n- Address system interactions and user experience."
            "\n- Ensure coverage of operational scenarios and key performance needs."
            "\n- Provide fundamental requirements before detailed engineering begins."

            "\n\n**Expected JSON Format:**"
            "{\n"
            "  \"headings\": [\"Water Tank Capacity\", \"Energy Efficiency\", \"Safety Features\", ...],\n"
            "  \"descriptions\": [\"The water tank shall have a minimum capacity of 1.5 liters.\", ...]\n"
            "}\n"
            "Ensure a maximum of 20 concept-level requirements."
            "Do NOT include numbering like 'Requirement 1', 'Requirement 2', etc."
            "Do NOT include citations like [1][3] or unnecessary text."
            "Respond ONLY with valid JSON in the format above."
        )
    },
    {"role": "user", "content": prompt}
]


    try:
        response = client.chat.completions.create(
            model="llama-3.1-sonar-large-128k-online",
            messages=messages
        )

        raw_output = response.choices[0].message.content.strip()

        # Extract valid JSON from the response
        start_index = raw_output.find("{")
        end_index = raw_output.rfind("}")
        if start_index != -1 and end_index != -1:
            json_string = raw_output[start_index:end_index + 1]
            parsed_json = json.loads(json_string)
            return parsed_json.get("headings", []), parsed_json.get("descriptions", [])
        else:
            st.error("AI response did not contain valid JSON.")
            return [], []

    except Exception as e:
        st.error(f"Error generating requirements: {e}")
        return [], []

# Function to open Gaphor application
def open_gaphor_app(gaphor_content):
    temp_dir = tempfile.gettempdir()
    gaphor_path = os.path.join(temp_dir, "temp_requirements.gaphor")
    with open(gaphor_path, 'w', encoding='utf-8') as f:
        f.write(gaphor_content)

    os_name = os.name
    if os_name == 'nt':  # Windows
        gaphor_executable = "C:\\Program Files\\Gaphor\\gaphor.exe"
    elif os_name == 'posix':  # macOS/Linux
        gaphor_executable = "/Applications/Gaphor.app/Contents/MacOS/Gaphor"
    else:
        st.error("Unsupported operating system.")
        return

    try:
        subprocess.run([gaphor_executable, gaphor_path], check=True)
        st.success("The file has been opened in the Gaphor application.")
    except FileNotFoundError:
        st.error(f"Gaphor executable not found at {gaphor_executable}. Please ensure it is installed correctly.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Main App
def main():
    st.title("MBSE Concept Level requirement Modeler for Gaphor")
    st.sidebar.title("How do you want to create the requirements diagram ?")
    
    MODES = {
        "manual": "📝 I will enter the requirements manually.",
        "ai": "🤖 Let AI generate the requirements for me.",
        "upload": "📂 Upload and Modify existing Gaphor file."
    }

    # Capture the previous mode to detect changes
    if 'previous_mode' not in st.session_state:
        st.session_state['previous_mode'] = ""

    mode = st.sidebar.radio("Choose an option:", list(MODES.values()))

    # Check if the mode has changed
    if mode != st.session_state['previous_mode']:
        st.session_state['gaphor_content'] = None  # Reset content
        st.session_state['previous_mode'] = mode   # Update the mode

    client = OpenAI(api_key= API_KEY, base_url="https://api.perplexity.ai")

    # Inside the upload mode block
    # Unified Edit/Delete/Add with Regenerate at once
    # Unified Edit/Delete/Add with Summary and Regenerate at once
    # Unified Edit/Delete/Add with Summary and Regenerate at once
    if mode == MODES["upload"]:
        st.header("Modify an Existing Gaphor Requirements File")
        uploaded_file = st.file_uploader("Upload your Gaphor (.gaphor) file", type=["gaphor", "xml"])

        if uploaded_file:
            gaphor_dict = xmltodict.parse(uploaded_file.read())

            try:
                requirements = gaphor_dict["gaphor"]["Requirement"]
                if isinstance(requirements, dict):
                    requirements = [requirements]
                headings = [r["name"]["val"] for r in requirements]
                descriptions = [r["text"]["val"] for r in requirements]

                if 'req_data' not in st.session_state:
                    st.session_state['req_data'] = [{"heading": h, "description": d} for h, d in zip(headings, descriptions)]
                if 'selected_to_edit' not in st.session_state:
                    st.session_state['selected_to_edit'] = []
                if 'selected_to_delete' not in st.session_state:
                    st.session_state['selected_to_delete'] = []
                if 'add_count' not in st.session_state:
                    st.session_state['add_count'] = 0
                if 'temp_edits' not in st.session_state:
                    st.session_state['temp_edits'] = {}

                with st.expander("📄 View Current Requirements Summary", expanded=False):
                    st.subheader("🧠 Summarized Requirements")
                    for i, (h, d) in enumerate(zip(headings, descriptions), 1):
                        st.markdown(f"**{i}. {h}**")
                        st.write(d)

                st.markdown("---")
                st.subheader("🛠 Edit / Delete / Add Requirements")

                # Delete selection
                all_headings = [r['heading'] for r in st.session_state['req_data']]
                st.session_state['selected_to_delete'] = st.multiselect("❌ Select requirements to delete", all_headings)

                # Filtered list for editing (exclude those marked for deletion)
                editable_headings = [h for h in all_headings if h not in st.session_state['selected_to_delete']]
                st.session_state['selected_to_edit'] = st.multiselect("✏️ Select requirements to edit", editable_headings, key="edit_select")

                for i, req in enumerate(st.session_state['req_data']):
                    if req['heading'] in st.session_state['selected_to_edit']:
                        edit_key = f"{req['heading']}_{i}"
                        if edit_key not in st.session_state['temp_edits']:
                            st.session_state['temp_edits'][edit_key] = {
                                "heading": req['heading'],
                                "description": req['description']
                            }

                        st.session_state['temp_edits'][edit_key]["heading"] = st.text_input(
                            f"Edit Heading {i+1}",
                            value=st.session_state['temp_edits'][edit_key]["heading"],
                            key=f"edit_heading_{edit_key}"
                        )

                        st.session_state['temp_edits'][edit_key]["description"] = st.text_area(
                            f"Edit Description {i+1}",
                            value=st.session_state['temp_edits'][edit_key]["description"],
                            key=f"edit_desc_{edit_key}"
                        )

                st.markdown("---")
                st.subheader("➕ Add New Requirements")
                st.session_state['add_count'] = st.number_input(
                    "How many requirements do you want to add?",
                    min_value=0, max_value=20, value=st.session_state['add_count']
                )
                new_reqs = []
                for i in range(st.session_state['add_count']):
                    new_heading = st.text_input(f"New Heading {i+1}", key=f"new_heading_{i}")
                    new_description = st.text_area(f"New Description {i+1}", key=f"new_desc_{i}")
                    new_reqs.append({"heading": new_heading, "description": new_description})

                if st.button("🚀 Regenerate Final Gaphor File"):
                    # STEP 1: Apply edits
                    updated_reqs = []
                    for i, req in enumerate(st.session_state['req_data']):
                        edit_key = f"{req['heading']}_{i}"
                        if edit_key in st.session_state.get('temp_edits', {}) and req['heading'] in st.session_state['selected_to_edit']:
                            edits = st.session_state['temp_edits'][edit_key]
                            updated_reqs.append({
                                "heading": edits["heading"],
                                "description": edits["description"]
                            })
                        else:
                            updated_reqs.append(req)

                    # STEP 2: Apply deletions
                    updated_reqs = [r for r in updated_reqs if r['heading'] not in st.session_state['selected_to_delete']]

                    # STEP 3: Apply additions
                    for r in new_reqs:
                        if r['heading'] and r['description']:
                            updated_reqs.append(r)

                    # STEP 4: Generate file
                    final_headings = [r['heading'] for r in updated_reqs]
                    final_descriptions = [r['description'] for r in updated_reqs]
                    st.session_state['gaphor_content'] = generate_gaphor_xml(final_headings, final_descriptions)
                    st.success("✅ File regenerated with all edits, deletions, and additions applied.")


            except Exception as e:
                st.error(f"❌ Could not process the uploaded Gaphor file: {e}")


    if mode == MODES["manual"]:
        st.header("Manual Requirements File Generator")
        num_requirements = st.number_input("Enter the number of requirements (up to 20):", min_value=1, max_value=20, step=1)
        
        headings = []
        descriptions = []
        
        for i in range(num_requirements):
            headings.append(st.text_input(f"Heading for Requirement {i + 1}", key=f"manual_heading_{i}"))
            descriptions.append(st.text_area(f"Description for Requirement {i + 1}", key=f"manual_description_{i}"))

        if st.button("Generate Gaphor File"):
            if headings and descriptions:
                st.session_state['gaphor_content'] = generate_gaphor_xml(headings, descriptions)


    if mode == MODES["ai"]:
        st.header("AI-Powered Requirements File Generator")
        prompt = st.text_area("Describe your requirements:", 
        placeholder="Example: I want requirements for a coffee machine.\nYou can also specify the number of requirements (up to 20).")

        if st.button("Generate AI-Based Gaphor File"):
            headings, descriptions = generate_requirements_from_llm(prompt, client)
            if headings and descriptions:
                st.session_state['gaphor_content'] = generate_gaphor_xml(headings, descriptions)


    if st.session_state.get('gaphor_content'):
        with st.container():  # Ensures layout stability
            col1, _ = st.columns(2)
            with col1:
                st.download_button(
                    label="⬇️ Download Gaphor File",
                    data=st.session_state['gaphor_content'],
                    file_name="requirements.gaphor",
                    mime="application/xml",
                    key="download_btn"
                )
        st.info("To view the diagram, download the file and open it using Gaphor installed on your local system.")
    
if __name__ == "__main__":
    main()
