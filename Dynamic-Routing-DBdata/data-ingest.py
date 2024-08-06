# insert the data to the postgresql database
import psycopg2

# Database connection parameters
HOST = "localhost"
DATABASE = "dynamicrouter"
USER = "postgres"
PASSWORD = "postgres"
PORT = "5432"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
    port=PORT
)
cursor = conn.cursor()

#Empty the Products table
cursor.execute("DROP TABLE IF EXISTS products")

#Empty langchain_pg_embedding table
cursor.execute("DROP TABLE IF EXISTS langchain_pg_embedding")

#commit
conn.commit()

# Create the Products table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) Unique,      
        price DECIMAL(10,2),
        category varchar(100)      
    )
""")

#List of products to insert
products_to_insert =[
    ("Medu Vada",50,"Starter" ),
    ("Gobi 65",70.00,"Starter"),
    ("Banana Bajiji",40,"Starter"),
    ("Paneer Pepper Fry",80,"Starter"),
    ("Masala Vada",50,"Starter"),
    ("Veg Fried Rice", 90, "Main Course"),
    ("Chicken Fried Rice", 110, "Main Course"),
    ("Chicken Biryani", 150, "Main Course"),
    ("Mutton Biryani", 180, "Main Course"),
    ("Egg Biryani", 140, "Main Course"),
    ("Veg Noodles", 100, "Main Course"),
    ("Chicken Noodles", 120, "Main Course"),
    ("Egg Noodles", 90, "Main Course"),
    ("Veg Manchurian", 80, "Main Course"),
    ("Chicken Manchurian", 110, "Main Course"),
    ("Egg Manchurian", 70, "Main Course"),
    ("Veg Spring Roll", 60, "Appetizer"),
    ("Chicken Spring Roll", 70, "Appetizer"),    
    ("Egg Spring Roll", 50, "Appetizer"),
    ("Veg Sushi Roll", 80, "Appetizer"),
    ("Chicken Sushi Roll", 100, "Appetizer"),
    ("Egg Sushi Roll", 70, "Appetizer"),
    ("Payasam",70,"Dessert"),
    ("Rasgulla",60,"Dessert"),
    ("Kulfi",50,"Dessert"),
    ("Gulab Jamun",80,"Dessert"),
    ("Rasmalai",90,"Dessert"),
    ("Kheer",100,"Dessert")
]
# Insert products into the Products table
for product in products_to_insert:
    cursor.execute("INSERT INTO products (name, price, category) VALUES (%s, %s, %s)", product)

# Commit the changes
conn.commit()
print("Data inserted successfully!")

#query the data
cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()
for row in rows:
    print(row)
    print("")

#close the connection
cursor.close()
conn.close()


