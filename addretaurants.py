import sqlite3

# Connect to the database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Get the criteria from the restaurant table in app.py
criteria = {
    'name': 'Jap de rouen',
    'address': '3 rue de l\'imagination Location',
    'cuisine': 'Japonnais',
    # Add more criteria here if needed
}

# Insert the restaurant into the database
cursor.execute("INSERT INTO restaurant (restaurantName, address, restaurantType) VALUES (?, ?, ?)",
               (criteria['name'], criteria['address'], criteria['cuisine']))

# Commit the changes and close the connection
conn.commit()
conn.close()
