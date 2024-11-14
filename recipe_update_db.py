import pandas as pd
import psycopg2
from psycopg2 import extras
from datetime import datetime as dt
import numpy as np

# Database connection setup
conn = psycopg2.connect(
    database="anyfeast-dev-db",
    user="admin_anyfeast",
    host="anyfeast-dev-db.postgres.database.azure.com",
    password="4VmSD).xk&KW,T-",
    port=5432
)

cur = conn.cursor()

# Load data from CSV
df = pd.read_csv("C:\\Users\\shwet\\Downloads\\not_match_recipe.csv")
df = df.iloc[207:212]  # Limiting to 2 rows for testing

# Clean up column names
df.columns = df.columns.str.strip()  # Clean up column names

# Remove any 'Unnamed' columns (those without headers or that are extra)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Fill in default values for missing or NaN data
df['steps'] = r"{}"  # Empty JSON
df['videos'] = r"{}"  # Empty JSON
df['images'] = r"{}"  # Empty JSON
df['allergy_info'] = r"{}"  # Empty JSON
df['createdAt'] = dt.now()
df['updatedAt'] = dt.now()

# Function to convert time to PostgreSQL interval format
def convert_to_interval(value):
    if pd.isna(value):  # Check if the value is NaN
        return None
    try:
        return f"{int(value)} minutes"  # Convert directly if it's already in minutes
    except ValueError:
        return None  # Handle any other unexpected cases

# Apply conversion to the relevant columns (e.g., 'cook_time' and 'prep_time')
# df['cook_time'] = df['cook_time'].apply(convert_to_interval)
# df['prep_time'] = df['prep_time'].apply(convert_to_interval)

# Replace NaN with None for nullable fields
df = df.replace({np.nan: None})

# Manually specify column names for insert
columns = ['name', 'description', 'calories', 'cuisine', 'cook_time', 'prep_time', 'ideal_consumer', 'ideal_time', 'veg', 'allergy_info', 'createdAt', 'updatedAt', 'active', 'country', 'steps', 'videos', 'images']
# Ensure column order matches the DataFrame's order
df = df[columns]

# Function to execute batch inserts
def execute_insert(conn, df, table):
    cursor = conn.cursor()
    
    # Build the insert query with explicit column names and values
    query = f"""
        INSERT INTO {table} (name, description, calories, cuisine, cook_time, prep_time, ideal_consumer, ideal_time, veg, allergy_info, "createdAt", "updatedAt", active, country, steps, videos, images)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
    """

    try:
        # Insert each row one by one (to handle any issues more gracefully)
        ids = []
        for index, row in df.iterrows():
            # Ensure all values are handled correctly
            cursor.execute(query, tuple(row))
            ids.append(cursor.fetchone()[0])
        
        conn.commit()
        cursor.close()
        return ids
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
        cursor.close()
        return None

# Insert all recipes one by one
new_ids = execute_insert(conn, df, "recipes")
if new_ids:
    print("Inserted rows:", new_ids)
else:
    print("No recipes were inserted.")

# Close connection
conn.close()
