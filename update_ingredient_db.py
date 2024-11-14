# # Part 2 Update name into DB
from os import name
import pandas as pd
import psycopg2
import psycopg2.extras as extras
 
df = pd.read_csv("C:\\any\\db\\product_match.csv")


df = df.iloc[:1]
 
sql = """ UPDATE ingredients
                
                SET price = %s
                WHERE id = %s"""
 
conn = psycopg2.connect(database = "anyfeast-dev-db",
                        user = "admin_anyfeast",
                        host= 'anyfeast-dev-db.postgres.database.azure.com',
                        password = "4VmSD).xk&KW,T-",
                        port = 5432)


 
cur = conn.cursor()
rows = [tuple(x) for x in df.values.tolist()]



for row in rows:
    # print("Row:", row)
    # print("Row Length:", len(row))
    cur.execute(sql, (row[-7], int(row[-1])))
 
conn.commit()
print('updated')

 

# Path to your CSV file
# df = pd.read_csv("matched_with_name.csv")


# df = df.iloc[245:]
# # Connect to your database
 
# conn = psycopg2.connect(database = "anyfeast-dev-db",
#                         user = "admin_anyfeast",
#                         host= 'anyfeast-dev-db.postgres.database.azure.com',
#                         password = "4VmSD).xk&KW,T-",
#                         port = 5432)
# cur = conn.cursor()

# # Define the SQL update statement
# sql_update = """
# UPDATE recipes
# SET name = %s, price = %s
# WHERE id = %s
# """

# # Read the CSV file and update the database
# for index, row in df.iterrows():
#     # Assuming your DataFrame has columns: id, name, price
#     ingredient_id = int(row['id'])  # Adjust the column names as necessary
#     name = row['name']               # Adjust the column names as necessary
#     price = float(row['price'])      # Adjust the column names as necessary
    
#     # Execute the update statement


#           # Adjust if your price is not the third column
        
#         # Execute the update statement
#     cur.execute(sql_update, (name,price,ingredient_id))

# # Commit the changes and close the connection
# conn.commit()
# cur.close()
# conn.close()
# print('update')
