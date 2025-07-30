import sqlite3

def read_fridge_metrics():
    conn = sqlite3.connect('temp/static/smart_fridge.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Products;")
    metrics = cursor.fetchall()
    
    for metric in metrics:
        print(metric)
    
    conn.close()

if __name__ == "__main__":
    read_fridge_metrics()