import sqlite3

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('smart_fridge.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Products table
    
    cursor.execute('drop table products')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_name TEXT,
            expiration_date DATE,
            barcode TEXT,
            nutritional_info TEXT,
            allergens TEXT,
            categories TEXT,
            image_url TEXT,
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    ''')

    # Create FridgeMetrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FridgeMetrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            temperature REAL,
            humidity REAL,
            light_status TEXT,
            pir_value BOOLEAN,
            recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

if __name__ == "__main__":
    create_database()