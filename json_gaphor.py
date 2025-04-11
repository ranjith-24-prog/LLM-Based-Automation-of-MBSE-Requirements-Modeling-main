import xmltodict
import json

# Function to convert JSON to XML (.gaphor)
def json_to_gaphor(json_file, gaphor_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            json_content = json.load(file)
        # Convert JSON (dict) to XML
        xml_content = xmltodict.unparse(json_content, pretty=True)
        # Write the XML content to a .gaphor file
        with open(gaphor_file, 'w', encoding='utf-8') as file:
            file.write(xml_content)
        print(f"Successfully converted {json_file} to {gaphor_file}")
    except Exception as e:
        print(f"Error converting JSON to Gaphor XML: {e}")

# Main function to demonstrate the usage
if __name__ == "__main__":
    # Replace with the full path to your JSON file
    json_input_file = r"Testing_now.json"  # Update this with your .json file path
    # Replace with the full path where you want the .gaphor output
    gaphor_output_file = r"Testing_now.gaphor"  # Update this with your desired .gaphor output path
    
    # Convert JSON to Gaphor XML
    json_to_gaphor(json_input_file, gaphor_output_file)