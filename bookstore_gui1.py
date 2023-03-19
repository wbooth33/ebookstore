import sqlite3
import tkinter as tk
from tkinter import messagebox

db = sqlite3.connect('C:/Users/will_/Documents/Hyperion Dev/T48/ebookstore.db')
cursor = db.cursor()

class BookstoreApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bookstore App!")

        # Set window dimensions and position
        window_width = 400
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create title label
        self.title_label = tk.Label(self, text="Bookstore App", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Create input fields
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)
        self.id_label = tk.Label(input_frame, text="ID:")
        self.id_label.grid(row=0, column=0)
        self.id_entry = tk.Entry(input_frame, width=30)
        self.id_entry.grid(row=0, column=1)
        self.title_label = tk.Label(input_frame, text="Title:")
        self.title_label.grid(row=1, column=0)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=1, column=1)
        self.author_label = tk.Label(input_frame, text="Author:")
        self.author_label.grid(row=2, column=0)
        self.author_entry = tk.Entry(input_frame, width=30)
        self.author_entry.grid(row=2, column=1)
        self.quantity_label = tk.Label(input_frame, text="Quantity:")
        self.quantity_label.grid(row=3, column=0)
        self.quantity_entry = tk.Entry(input_frame, width=30)
        self.quantity_entry.grid(row=3, column=1)

        # Create buttons frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # Create buttons
        self.add_button = tk.Button(button_frame, text="Add Book", width=10, command=self.add_book)
        self.add_button.grid(row=0, column=0, padx=5)
        self.update_button = tk.Button(button_frame, text="Update Book", width=10, command=self.update_book)
        self.update_button.grid(row=0, column=1, padx=5)
        self.search_button = tk.Button(button_frame, text="Search Book", width=10, command=self.search_book)
        self.search_button.grid(row=0, column=2, padx=5)
        self.delete_button = tk.Button(button_frame, text="Delete Book", width=10, command=self.delete_book)
        self.delete_button.grid(row=0, column=3, padx=5)

        # Center input frame
        input_frame.place(relx=0.5, rely=0.35, anchor="center")
        # Center button frame
        button_frame.place(relx=0.5, rely=0.75, anchor="center")




    def add_book(self):
        id = self.id_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()
        quantity = self.quantity_entry.get()

        cursor.execute('''INSERT INTO books (id, title, author, quantity) VALUES (?,?,?,?)''', (id, title, author, quantity))
        db.commit()

        tk.messagebox.showinfo("Book Added", f"{quantity} copies of {title} by {author} have been added under ID: {id}")

    def update_book(self):
        id = self.id_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()
        quantity = self.quantity_entry.get()

        update_fields = []
        if title:
            update_fields.append(f"title='{title}'")
        if author:
            update_fields.append(f"author='{author}'")
        if quantity:
            update_fields.append(f"quantity={quantity}")
        if not update_fields:
            tk.messagebox.showwarning("No Fields to Update", "Please enter at least one field to update.")
            return

        update_query = "UPDATE books SET " + ", ".join(update_fields) + f" WHERE id={id}"
        cursor.execute(update_query)
        db.commit()

        tk.messagebox.showinfo("Book Updated", f"Book with ID: {id} updated.")

    def search_book(self):
        id = self.id_entry.get()
        cursor.execute(f"SELECT * FROM books WHERE id={id}")
        result = cursor.fetchone()

        if result:
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)

            self.title_entry.insert(0, result[1])
            self.author_entry.insert(0, result[2])
            self.quantity_entry.insert(0, result[3])

            tk.messagebox.showinfo("Book Found", f"Title: {result[1]}\nAuthor: {result[2]}\nQuantity: {result[3]}")
        else:
            tk.messagebox.showerror("Book Not Found", f"Book with ID: {id} not found.")

    def delete_book(self):
        id = self.id_entry.get()

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete book with ID: {id}?")
        if confirm:
            cursor.execute(f"DELETE FROM books WHERE id={id}")
            db.commit()
            messagebox.showinfo("Book Deleted", f"Book with ID: {id} has been deleted from the database.")


if __name__ == '__main__':
    app = BookstoreApp()
    app.mainloop()
