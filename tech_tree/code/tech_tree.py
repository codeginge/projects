""" 
OVERVIEW: this code creates a visual tech (technology) tree for techs learned in robotics 
and organizes them based on their dependent techs. this code will:

1. opens a google sheet with this data structure:
|--name--|--type--|--difficulty--|--letter--|--num--|--id--|--depends--|--notes--|

2. creates a json file from the goolge sheet with this data stucture:

"robotics/other/techs.json"
[
	{
		"name":"Light - LED", 
		"type":"actuators", 
		"difficulty":1,
		"id":"a1_01", 
		"depends":["c1_01","c1_02","c1_03"],
		"notes":"Basic light-emitting diode for signaling or lighting in various colors."
	},
	{
		"name":"Barometric Pressure and Temperature - BMP280", 
		"type":"sensors", 
		"difficulty":2,
		"id":"s2_02", 
		"dependent_on":["s1","s1_10","s1_11","s1_05"],
		"notes":"Improved version of BMP180 with temperature readings."
	}
]

3. sorts the technologies by difficulty, then type, and then by dependencies. 

4. creates a tech tree visual from the dependency sorted list and outputs it in 


Example CMD:
python3 -m venv myenv && source myenv/bin/activate && pip install graphviz && pip show graphviz
python3 ./tech_tree.py ../../../../Downloads/circuits_tech_tree-techDataSheet.csv ../other/techs.json
"""
import csv
import json
import argparse
from graphviz import Digraph

# Set up argument parsing to accept both CSV file path and JSON output file name
parser = argparse.ArgumentParser(description="Convert Arduino Tech Tree CSV to JSON format.")
parser.add_argument("csv_file", help="Path to the CSV file")
parser.add_argument("json_file", help="Path to the output JSON file")
args = parser.parse_args()

# Path to the CSV file and output JSON file passed via command line
csv_file_path = args.csv_file
json_file_path = args.json_file

# Open and read the CSV file
formatted_data = []

with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)  # Read the CSV as a dictionary
    
    # Skip the first row (filename row)
    next(csv_file)
    
    # Ensure the 'depends' column exists
    if 'depends' not in csv_reader.fieldnames:
        print("Warning: 'depends' column is missing in the CSV file.")
    
    for row in csv_reader:
        # Safely handle the "depends" column (space-separated values)
        depends = []
        if 'depends' in row and row['depends']:  # Check if 'depends' column exists and is not empty
            depends = [dep.strip() for dep in row["depends"].split()]
        
        # Format the data into the desired structure
        formatted_data.append({
            "name": row.get("name", ""),
            "type": row.get("type", ""),
            "difficulty": int(row.get("difficulty", "0").split("_")[0]),  # Default to 0 if missing
            "id": f"{row.get('letter', '')}_{row.get('num', '')}",
            "depends": depends,  # Now depends is a list from the space-separated values
            "notes": row.get("notes", "")
        })

# Output the data to the specified JSON file
with open(json_file_path, "w") as json_file:
    json.dump(formatted_data, json_file, indent=4)

print(f"Data has been written to {json_file_path}")


def create_flowchart(data, output_file):
    # Initialize the graph
    dot = Digraph(format="png")
    dot.attr(rankdir="TB")  # Top-to-bottom layout
    dot.attr("node", shape="box", style="filled", fontname="Arial")
    dot.attr(splines="false")  # Disable curved edges, force straight lines

    # Set the separation values to avoid overlap but keep things closer
    dot.attr(ranksep="0.6")  # Decrease vertical distance between ranks (levels)
    dot.attr(nodesep="0.3")  # Decrease horizontal space between nodes

    # Define colors for each type
    type_colors = {
        "actuators": "lightgreen",
        "sensors": "lightblue",
        "programming": "lightyellow",
        "wiring": "lightseagreen",
        "circuit_knowledge": "lightpink",
        # Add more types and their respective colors as needed
    }

    # Group nodes by difficulty and type
    difficulty_groups = {1: {}, 2: {}, 3: {}}
    for item in data:
        difficulty = item["difficulty"]
        item_type = item["type"]
        
        # Create a dictionary for each difficulty with item types as the key
        if item_type not in difficulty_groups[difficulty]:
            difficulty_groups[difficulty][item_type] = []
        
        difficulty_groups[difficulty][item_type].append(item)

    # Add nodes grouped by difficulty and enforce vertical stacking
    for difficulty in range(1, 4):  # Explicitly iterate over difficulties 1, 2, 3
        items = []
        for item_type, type_items in difficulty_groups[difficulty].items():
            # Choose color based on item type
            type_color = type_colors.get(item_type, "lightgray")  # Default to lightgray if no color defined

            with dot.subgraph() as sub:
                sub.attr(rank="same")  # Enforce same rank for all nodes in this difficulty level
                sub.attr(labeljust="c")  # Center align the types horizontally
                sub.attr(style="dashed")  # Add dashed style to indicate separation

                # Add each node with the fillcolor applied to the node individually
                for item in type_items:
                    # Set a reasonable width and height for nodes
                    sub.node(item["id"], f'{item["name"]}\n({item["id"]})', fillcolor=type_color, width="1", height="0.4")
                items.extend(type_items)

        # Add dependencies between same type difficulty levels with invisible arrows
        if difficulty > 1:  # If difficulty is 2 or 3, add dependencies to previous level
            for item in items:
                for prev_item in difficulty_groups[difficulty - 1].get(item["type"], []):
                    dot.edge(prev_item["id"], item["id"], style="invisible", dir="none", minlen="1.5", weight="0")  # Invisible edge with no arrowhead

    # Add edges for the visible dependencies from JSON data (these should be shown)
    for item in data:
        for dependency in item["depends"]:
            dot.edge(dependency, item["id"], minlen="1.5", weight="1")  # Regular visible edges with space between nodes

    # Save and render the graph
    dot.render(output_file, cleanup=True)
    print(f"Flowchart saved to {output_file}.png")





# Create the flowchart
flowchart_filename = "../other/techTree"
create_flowchart(formatted_data,flowchart_filename)
