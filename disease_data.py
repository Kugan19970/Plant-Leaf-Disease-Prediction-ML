import pandas as pd

# Load disease details from the Excel file
file_path = "disease_data.xlsx"  # Ensure this file is in the same directory or provide a full path
df = pd.read_excel(file_path)

# Convert DataFrame to a dictionary with numerical keys
disease_details = {
    index: {
        "name": row["name"],
        "description": row["description"],
        "solution": row["solution"],
        "recommendations": row["recommendations"].split("\n") if isinstance(row["recommendations"], str) else []
    }
    for index, row in df.iterrows()
}

def get_disease_details(class_id):
    """
    Get disease details based on the class ID from the Excel file.
    
    :param class_id: Predicted class ID from the model.
    :return: A dictionary containing the disease name, description, solution, and recommendations.
    """
    return disease_details.get(class_id, {
        "name": "Unknown Disease",
        "description": "No description available.",
        "solution": "No solution available.",
        "recommendations": []
    })
