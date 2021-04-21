from transitracker import db
try:
    db.create_all()
    print("Tables created successfully.")
except:
    print("Table creation failed.")