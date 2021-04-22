#author:            Trevor STrobel

#this is just a quick script to drop db tables. It should only be used in development
from transitracker import db

print("Agreeing to run this script will drop all tables from this application's database.")
print("That means all user data is deleted. Think before you delete.")

while True:

    val = input("Would you like to drop all tables? y/n :")


    if val == 'y':
        db.drop_all()
        print("Tables Dropped")
        quit()
    elif val == 'n':
        print("Tables NOT dropped")
        quit()
    else:
        print("please enter y or n")
