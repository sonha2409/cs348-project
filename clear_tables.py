import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('tennis.db')
cursor = conn.cursor()

# List of tables for which we want to delete all entries
tables = ['players', 'tournaments', 'matches', 'rankings', 'player_statistics', 'tournament_standings']

# Execute a DELETE statement for each table
for table in tables:
    try:
        cursor.execute(f'DELETE FROM {table};')
        print(f"All data from table '{table}' has been deleted.")
    except sqlite3.Error as e:
        print(f"An error occurred while deleting data from table '{table}': {e}")

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("All data has been cleaned from the database.")
