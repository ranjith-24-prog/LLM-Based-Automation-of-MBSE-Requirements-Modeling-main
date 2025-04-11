import xmltodict
import json

# Function to convert XML (.gaphor) to JSON
def xml_to_json(xml_file, json_file):
    try:
        with open(xml_file, 'r', encoding='utf-8') as file:
            xml_content = file.read()
        # Convert XML content to a Python dictionary
        data_dict = xmltodict.parse(xml_content)
        # Convert dictionary to JSON
        json_content = json.dumps(data_dict, indent=4)
        with open(json_file, 'w', encoding='utf-8') as file:
            file.write(json_content)
        print(f"Successfully converted {xml_file} to {json_file}")
    except Exception as e:
        print(f"Error converting XML to JSON: {e}")

# Main function to demonstrate the usage
if __name__ == "__main__":
    # Replace with the full path to your .gaphor file
    xml_input_file = r"Template1.gaphor"  # Update this with your .gaphor file path
    # Replace with the full path where you want the JSON output
    json_output_file = r"Template1.json"  # Update this with your desired output path
    
    # Convert XML to JSON
    xml_to_json(xml_input_file, json_output_file)
