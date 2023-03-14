#Import SQLite3 and connect to the database.
import sqlite3

db = sqlite3.connect('C:/Users/will_/Documents/Hyperion Dev/T48/ebookstore.db')

cursor = db.cursor()

#Define a function to add a new book to database.
def add_book(id, title, author, quantity):
    cursor.execute('''INSERT INTO books (id, title, author, quantity) VALUES (?,?,?,?)''', (id, title, author, quantity))
    db.commit()
    print(f'ID: {id}\nTitle: {title}\nAuthor: {author}\nQuantity: {quantity}\n')
    print(f'{quantity} copies of {title} by {author} have been successfully added under ID: {id}')

#Define a function to update a book in the database.
def update_book(id, title=None, author=None, quantity=None):
    update_fields = []
    if title:
        update_fields.append(f"title='{title}'")
    if author:
        update_fields.append(f"author='{author}'")
    if quantity:
        update_fields.append(f"quantity={quantity}")
    if not update_fields:
        print("No fields to update.")
        return
    update_query = "UPDATE books SET " + ", ".join(update_fields) + f" WHERE id={id}"
    cursor.execute(update_query)
    db.commit()
    print(f"Book with ID: {id} updated.\n")

#Define a function to delete books from the database.
def delete_book(id):
    cursor.execute(f"SELECT title, author FROM books WHERE id={id}")
    book = cursor.fetchone()
    if not book:
        print(f"Book with id={id} not found in the database.\n")
        return
    cursor.execute(f"DELETE FROM books WHERE id={id}")
    db.commit()
    print(f"Book '{book[0]}' by {book[1]} deleted from the database.\n")

#Define a function to search for books in the database with an empty list to store input information.
def search_books(title=None, author=None):
    search_fields = []
    if title:
        search_fields.append(f"title='{title}'")
    if author:
        search_fields.append(f"author='{author}'")
    #If no information entered into search fields. Error.
    if not search_fields:
        print("No search criteria specified.")
        return
    search_query = "SELECT * FROM books WHERE " + " AND ".join(search_fields)
    cursor.execute(search_query)
    results = cursor.fetchall()
    #If no book found in database.
    if not results:
        print("No books found in the database.\n")
        return
    print("Books found in the database:")
    for row in results:
        print(f"\nID: {row[0]}\nTitle: {row[1]}\nAuthor: {row[2]}\nQuantity: {row[3]}")
    print()

#Create table called books with ID, Title, Author and Quantity. Use try/except to see if table already exists or not.
try:
    cursor.execute('''
        CREATE TABLE books (
            ID INTEGER PRIMARY KEY,
            Title TEXT,
            Author TEXT,
            Quantity INTEGER
        )
    ''')
    print('Table created successfully')
except sqlite3.OperationalError as e:
    if 'table books already exists' in str(e):
        print('Table already exists')
    else:
        print('Error creating table:', e)

#Information to be added into the database.
id1 = 3001
title1 = 'A Tale of Two Cities'
author1 = 'Charles Dickens'
quantity1 = 30

id2 = 3002
title2 = 'Harry Potter and the Philospher\'s Stone'
author2 = 'J.K. Rowling'
quantity2 = 40

id3 = 3003
title3 = 'The Lion, the witch and the Wardrobe'
author3 = 'C.S. Lewis'
quantity3 = 25

id4 = 3004
title4 = 'The Lord of the Rings'
author4 = 'J.R.R Tolkien'
quantity4 = 37

id5 = 3005
title5 = 'Alice in Wonderland'
author5 = 'Lewis Carroll'
quantity5 = 12

#Insert the data for all books into the database.
book_info = [(id1,title1,author1,quantity1),(id2,title2,author2,quantity2),(id3,title3,author3,quantity3),(id4,title4,author4,quantity4),(id5,title5,author5,quantity5)]
cursor.executemany('''INSERT OR IGNORE INTO books (id,title,author,quantity) VALUES (?,?,?,?)''',(book_info))

#Commit information to database.
db.commit()

#Define main function with the menu for the program.
def main():
    try:
        while True:
            print('''\nBookstore Management System!
            1 - Add a book!
            2 - Update a book!
            3 - Delete a book!
            4 - Search for a book!
            5 - Exit!
            ''')
            #Ask user what menu option the want to choose.
            choice = input("Enter your choice:\n")
            #If choice is "1", ask user for book id, title, author and quantity. Call function to add book to database.
            if choice == "1":
                print("Adding a book to the database!")
                id = int(input("Enter the book id:\n"))
                title = input("Enter book title:\n")
                author = input("Enter book author:\n")
                quantity = int(input("Enter book quantity:\n"))
                add_book(id, title, author, quantity)

            #Else if choice is "2", ask user for the book id, title, author and quantity leaving blank anything not wanting to update. Call function for updating book.
            elif choice == "2":
                print("Updating a book in the Database!")
                id = int(input("Enter book ID:\n"))
                title = input("Enter new title (leave blank to keep existing title):\n")
                author = input("Enter new author (leave blank to keep existing author):\n")
                quantity = input("Enter new quantity (leave blank to keep existing quantity):\n")
                if quantity:
                    quantity = int(quantity)
                    update_book(id, title, author, quantity)

            #Else if choice is "3", ask user to enter ID of the book to delete. Call function to delete book.
            elif choice == "3":
                Print("Delete a book from the database!")
                book_id = input("Enter the ID of the book you want to delete:\n")
                delete_book(book_id)

            #Else if choice is "4", ask user the book title or author to search for in database. Call function to search for a book.
            elif choice == "4":
                print("Search for a book in the Database!")
                title = input("Enter the book title (or leave blank to skip):\n")
                author = input("Enter the book author (or leave blank to skip):\n")
                search_books(title=title, author=author)

            #Else if choice is "5", exit the program.
            elif choice == "5":
                print("Exiting the program...")
                break
            
            #Else invalid choice.
            else:
                print("Invalid choice, please try again.")
    #Finally close database.
    finally:
        db.close()
#Call function for main.
if __name__ == '__main__':
    main()










