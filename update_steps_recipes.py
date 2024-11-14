import pandas as pd
import psycopg2
import psycopg2.extras

# Define the path to your CSV file
excel_file_path = r"C:\\Users\\shwet\\Downloads\\not_match_recipe.csv"

# Load the CSV file
df = pd.read_csv(excel_file_path, encoding='ISO-8859-1')
# df = df.iloc[:2]  # Adjust the rows as necessary

# Connect to PostgreSQL
conn = psycopg2.connect(
    database="anyfeast-dev-db",
    user="admin_anyfeast",
    host="anyfeast-dev-db.postgres.database.azure.com",
    password="4VmSD).xk&KW,T-",
    port=5432
)

# Create a cursor object
cursor = conn.cursor()

# Iterate through the dataframe and insert the data
for index, row in df.iterrows():
    recipe_name = row['name']
    steps = row['steps']

    # Skip invalid steps (such as NaN or non-list data)
    if not steps or pd.isna(steps):
        print(f"Skipping invalid data for recipe '{recipe_name}'")
        continue

    # Convert the 'steps' field to a Python list (assuming it's a string representation of a list)
    try:
        steps_list = eval(steps) if isinstance(steps, str) else steps  # Assuming steps are in a list-like format
    except Exception as e:
        print(f"Error parsing steps for recipe '{recipe_name}': {e}")
        continue  # Skip invalid rows and move to the next

    # SQL query to search for the recipe by name
    search_query = """
    SELECT id FROM recipes WHERE name = %s;
    """
    cursor.execute(search_query, (recipe_name,))
    
    result = cursor.fetchone()  # Fetch the first result
    
    if result:
        # If a matching recipe is found, insert the steps for that recipe
        recipe_id = result[0]
        
        # Convert Python list to PostgreSQL array format (use psycopg2.extras)
        try:
            update_query = """
            UPDATE recipes
            SET steps = %s
            WHERE id = %s;
            """
            cursor.execute(update_query, (steps_list, recipe_id))
            print(f"Steps for recipe '{recipe_name}' have been updated.")
        except Exception as e:
            print(f"Error updating steps for recipe '{recipe_name}': {e}")
    else:
        print(f"No matching recipe found for '{recipe_name}'.")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
