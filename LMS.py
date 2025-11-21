import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        self.init_database()
    
        self.create_gui()
        
        self.load_books()
        self.load_members()
        self.load_issued_books()
    
    def init_database(self):
        """Initialize SQLite database and create tables"""
        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()
       
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                quantity INTEGER NOT NULL,
                available INTEGER NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                membership_date TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS issued_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books (id),
                FOREIGN KEY (member_id) REFERENCES members (id)
            )
        ''')
        
        self.conn.commit()
    
    def create_gui(self):
        """Create the main GUI interface"""
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
       
        self.books_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.books_frame, text='Books')
        self.create_books_tab()
       
        self.members_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.members_frame, text='Members')
        self.create_members_tab()
       
        self.issue_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.issue_frame, text='Issue/Return')
        self.create_issue_tab()
       
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text='Reports')
        self.create_reports_tab()
    
    def create_books_tab(self):
        """Create the books management interface"""
        
        add_frame = ttk.LabelFrame(self.books_frame, text="Add New Book")
        add_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(add_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.title_entry = ttk.Entry(add_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Author:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.author_entry = ttk.Entry(add_frame, width=30)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(add_frame, text="ISBN:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.isbn_entry = ttk.Entry(add_frame, width=30)
        self.isbn_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Quantity:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.quantity_entry = ttk.Entry(add_frame, width=30)
        self.quantity_entry.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Button(add_frame, text="Add Book", command=self.add_book).grid(row=2, column=3, padx=5, pady=5, sticky='e')
        
        list_frame = ttk.LabelFrame(self.books_frame, text="Book List")
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('id', 'title', 'author', 'isbn', 'quantity', 'available')
        self.books_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        self.books_tree.heading('id', text='ID')
        self.books_tree.heading('title', text='Title')
        self.books_tree.heading('author', text='Author')
        self.books_tree.heading('isbn', text='ISBN')
        self.books_tree.heading('quantity', text='Quantity')
        self.books_tree.heading('available', text='Available')
        
        self.books_tree.column('id', width=50)
        self.books_tree.column('title', width=200)
        self.books_tree.column('author', width=150)
        self.books_tree.column('isbn', width=100)
        self.books_tree.column('quantity', width=80)
        self.books_tree.column('available', width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        
        self.books_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        ttk.Button(list_frame, text="Delete Selected", command=self.delete_book).pack(side='bottom', pady=5)
    
    def create_members_tab(self):
        """Create the members management interface"""
        
        add_frame = ttk.LabelFrame(self.members_frame, text="Add New Member")
        add_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.member_name_entry = ttk.Entry(add_frame, width=30)
        self.member_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Email:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.email_entry = ttk.Entry(add_frame, width=30)
        self.email_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.phone_entry = ttk.Entry(add_frame, width=30)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(add_frame, text="Add Member", command=self.add_member).grid(row=1, column=3, padx=5, pady=5, sticky='e')
        
        list_frame = ttk.LabelFrame(self.members_frame, text="Member List")
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('id', 'name', 'email', 'phone', 'membership_date')
        self.members_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        self.members_tree.heading('id', text='ID')
        self.members_tree.heading('name', text='Name')
        self.members_tree.heading('email', text='Email')
        self.members_tree.heading('phone', text='Phone')
        self.members_tree.heading('membership_date', text='Member Since')
        
        self.members_tree.column('id', width=50)
        self.members_tree.column('name', width=150)
        self.members_tree.column('email', width=200)
        self.members_tree.column('phone', width=120)
        self.members_tree.column('membership_date', width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=scrollbar.set)
        
        self.members_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        ttk.Button(list_frame, text="Delete Selected", command=self.delete_member).pack(side='bottom', pady=5)
    
    def create_issue_tab(self):
        """Create the book issue/return interface"""
        
        issue_frame = ttk.LabelFrame(self.issue_frame, text="Issue Book")
        issue_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(issue_frame, text="Member:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.issue_member_combo = ttk.Combobox(issue_frame, state="readonly")
        self.issue_member_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(issue_frame, text="Book:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.issue_book_combo = ttk.Combobox(issue_frame, state="readonly")
        self.issue_book_combo.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(issue_frame, text="Issue Book", command=self.issue_book).grid(row=0, column=4, padx=5, pady=5)
        
        return_frame = ttk.LabelFrame(self.issue_frame, text="Return Book")
        return_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(return_frame, text="Issued Book:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.return_combo = ttk.Combobox(return_frame, state="readonly", width=50)
        self.return_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(return_frame, text="Return Book", command=self.return_book).grid(row=0, column=2, padx=5, pady=5)
        
        list_frame = ttk.LabelFrame(self.issue_frame, text="Currently Issued Books")
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('id', 'book_title', 'member_name', 'issue_date', 'due_date')
        self.issued_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        self.issued_tree.heading('id', text='ID')
        self.issued_tree.heading('book_title', text='Book Title')
        self.issued_tree.heading('member_name', text='Member Name')
        self.issued_tree.heading('issue_date', text='Issue Date')
        self.issued_tree.heading('due_date', text='Due Date')
        
        self.issued_tree.column('id', width=50)
        self.issued_tree.column('book_title', width=200)
        self.issued_tree.column('member_name', width=150)
        self.issued_tree.column('issue_date', width=100)
        self.issued_tree.column('due_date', width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.issued_tree.yview)
        self.issued_tree.configure(yscrollcommand=scrollbar.set)
        
        self.issued_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_reports_tab(self):
        """Create the reports interface"""
       
        reports_frame = ttk.Frame(self.reports_frame)
        reports_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Button(reports_frame, text="Books Report", command=self.generate_books_report, width=20).pack(pady=5)
        ttk.Button(reports_frame, text="Members Report", command=self.generate_members_report, width=20).pack(pady=5)
        ttk.Button(reports_frame, text="Issued Books Report", command=self.generate_issued_report, width=20).pack(pady=5)
        ttk.Button(reports_frame, text="Overdue Books", command=self.generate_overdue_report, width=20).pack(pady=5)
        
        self.report_text = tk.Text(reports_frame, height=20, width=80)
        self.report_text.pack(pady=10, fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(self.report_text, orient='vertical', command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
    
    def load_books(self):
        """Load books from database into the treeview"""
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        
        for book in books:
            self.books_tree.insert('', 'end', values=book)
        
        self.cursor.execute("SELECT id, title FROM books WHERE available > 0")
        available_books = self.cursor.fetchall()
        self.issue_book_combo['values'] = [f"{book[0]} - {book[1]}" for book in available_books]
    
    def load_members(self):
        """Load members from database into the treeview"""
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        
        self.cursor.execute("SELECT * FROM members")
        members = self.cursor.fetchall()
        
        for member in members:
            self.members_tree.insert('', 'end', values=member)
        
        self.issue_member_combo['values'] = [f"{member[0]} - {member[1]}" for member in members]
    
    def load_issued_books(self):
        """Load issued books from database into the treeview"""
        for item in self.issued_tree.get_children():
            self.issued_tree.delete(item)
        
        self.cursor.execute('''
            SELECT ib.id, b.title, m.name, ib.issue_date, ib.due_date 
            FROM issued_books ib
            JOIN books b ON ib.book_id = b.id
            JOIN members m ON ib.member_id = m.id
            WHERE ib.return_date IS NULL
        ''')
        issued_books = self.cursor.fetchall()
        
        for book in issued_books:
            self.issued_tree.insert('', 'end', values=book)
        
        self.return_combo['values'] = [f"{book[0]} - {book[1]} (by {book[2]})" for book in issued_books]
    
    def add_book(self):
        """Add a new book to the database"""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        
        if not title or not author or not isbn or not quantity:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer")
            return
        
        try:
            self.cursor.execute(
                "INSERT INTO books (title, author, isbn, quantity, available) VALUES (?, ?, ?, ?, ?)",
                (title, author, isbn, quantity, quantity)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Book added successfully")
            
            self.title_entry.delete(0, 'end')
            self.author_entry.delete(0, 'end')
            self.isbn_entry.delete(0, 'end')
            self.quantity_entry.delete(0, 'end')
            
            self.load_books()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "A book with this ISBN already exists")
    
    def delete_book(self):
        """Delete the selected book from the database"""
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a book to delete")
            return
        
        book_id = self.books_tree.item(selected[0])['values'][0]
        
        self.cursor.execute("SELECT COUNT(*) FROM issued_books WHERE book_id = ? AND return_date IS NULL", (book_id,))
        count = self.cursor.fetchone()[0]
        
        if count > 0:
            messagebox.showerror("Error", "Cannot delete book that is currently issued")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            self.conn.commit()
            self.load_books()
    
    def add_member(self):
        """Add a new member to the database"""
        name = self.member_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        if not name or not email:
            messagebox.showerror("Error", "Name and email are required")
            return
        
        membership_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            self.cursor.execute(
                "INSERT INTO members (name, email, phone, membership_date) VALUES (?, ?, ?, ?)",
                (name, email, phone, membership_date)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Member added successfully")
            
            self.member_name_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.phone_entry.delete(0, 'end')
            
            self.load_members()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "A member with this email already exists")
    
    def delete_member(self):
        """Delete the selected member from the database"""
        selected = self.members_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a member to delete")
            return
        
        member_id = self.members_tree.item(selected[0])['values'][0]
        
        self.cursor.execute("SELECT COUNT(*) FROM issued_books WHERE member_id = ? AND return_date IS NULL", (member_id,))
        count = self.cursor.fetchone()[0]
        
        if count > 0:
            messagebox.showerror("Error", "Cannot delete member who has issued books")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this member?"):
            self.cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
            self.conn.commit()
            self.load_members()
    
    def issue_book(self):
        """Issue a book to a member"""
        member_selection = self.issue_member_combo.get()
        book_selection = self.issue_book_combo.get()
        
        if not member_selection or not book_selection:
            messagebox.showerror("Error", "Please select both a member and a book")
            return
        
        member_id = int(member_selection.split(' - ')[0])
        book_id = int(book_selection.split(' - ')[0])
        
        self.cursor.execute(
            "SELECT COUNT(*) FROM issued_books WHERE member_id = ? AND return_date IS NULL", 
            (member_id,)
        )
        borrowed_count = self.cursor.fetchone()[0]
        
        if borrowed_count >= 5:
            messagebox.showerror("Error", "Member has reached the maximum borrowing limit (5 books)")
            return
        
        issue_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d") 
        
        try:
            self.cursor.execute(
                "INSERT INTO issued_books (book_id, member_id, issue_date, due_date) VALUES (?, ?, ?, ?)",
                (book_id, member_id, issue_date, due_date)
            )
            
            self.cursor.execute(
                "UPDATE books SET available = available - 1 WHERE id = ?",
                (book_id,)
            )
            
            self.conn.commit()
            messagebox.showinfo("Success", f"Book issued successfully. Due date: {due_date}")
            
            self.load_books()
            self.load_issued_books()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
    
    def return_book(self):
        """Return an issued book"""
        selection = self.return_combo.get()
        if not selection:
            messagebox.showerror("Error", "Please select a book to return")
            return
        
        issue_id = int(selection.split(' - ')[0])
        return_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            self.cursor.execute("SELECT book_id FROM issued_books WHERE id = ?", (issue_id,))
            book_id = self.cursor.fetchone()[0]
            
            self.cursor.execute(
                "UPDATE issued_books SET return_date = ? WHERE id = ?",
                (return_date, issue_id)
            )
            
            self.cursor.execute(
                "UPDATE books SET available = available + 1 WHERE id = ?",
                (book_id,)
            )
            
            self.conn.commit()
            messagebox.showinfo("Success", "Book returned successfully")
            
            self.load_books()
            self.load_issued_books()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
    
    def generate_books_report(self):
        """Generate a report of all books"""
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        
        report = "BOOKS REPORT\n"
        report += "=" * 50 + "\n"
        report += f"{'ID':<5} {'Title':<30} {'Author':<20} {'ISBN':<15} {'Qty':<5} {'Avail':<5}\n"
        report += "-" * 85 + "\n"
        
        for book in books:
            report += f"{book[0]:<5} {book[1][:29]:<30} {book[2][:19]:<20} {book[3]:<15} {book[4]:<5} {book[5]:<5}\n"
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    def generate_members_report(self):
        """Generate a report of all members"""
        self.cursor.execute("SELECT * FROM members")
        members = self.cursor.fetchall()
        
        report = "MEMBERS REPORT\n"
        report += "=" * 50 + "\n"
        report += f"{'ID':<5} {'Name':<25} {'Email':<25} {'Phone':<15} {'Member Since':<12}\n"
        report += "-" * 85 + "\n"
        
        for member in members:
            report += f"{member[0]:<5} {member[1][:24]:<25} {member[2][:24]:<25} {member[3]:<15} {member[4]:<12}\n"
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    def generate_issued_report(self):
        """Generate a report of all issued books"""
        self.cursor.execute('''
            SELECT ib.id, b.title, m.name, ib.issue_date, ib.due_date, ib.return_date
            FROM issued_books ib
            JOIN books b ON ib.book_id = b.id
            JOIN members m ON ib.member_id = m.id
            ORDER BY ib.issue_date DESC
        ''')
        issued_books = self.cursor.fetchall()
        
        report = "ISSUED BOOKS REPORT\n"
        report += "=" * 50 + "\n"
        report += f"{'ID':<5} {'Book':<25} {'Member':<20} {'Issue Date':<12} {'Due Date':<12} {'Return Date':<12}\n"
        report += "-" * 90 + "\n"
        
        for book in issued_books:
            return_date = book[5] if book[5] else "Not Returned"
            report += f"{book[0]:<5} {book[1][:24]:<25} {book[2][:19]:<20} {book[3]:<12} {book[4]:<12} {return_date:<12}\n"
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    def generate_overdue_report(self):
        """Generate a report of overdue books"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute('''
            SELECT ib.id, b.title, m.name, ib.issue_date, ib.due_date
            FROM issued_books ib
            JOIN books b ON ib.book_id = b.id
            JOIN members m ON ib.member_id = m.id
            WHERE ib.due_date < ? AND ib.return_date IS NULL
            ORDER BY ib.due_date
        ''', (today,))
        
        overdue_books = self.cursor.fetchall()
        
        report = "OVERDUE BOOKS REPORT\n"
        report += "=" * 50 + "\n"
        
        if not overdue_books:
            report += "No overdue books.\n"
        else:
            report += f"{'ID':<5} {'Book':<25} {'Member':<20} {'Issue Date':<12} {'Due Date':<12} {'Days Overdue':<12}\n"
            report += "-" * 90 + "\n"
            
            for book in overdue_books:
                due_date = datetime.strptime(book[4], "%Y-%m-%d")
                days_overdue = (datetime.now() - due_date).days
                report += f"{book[0]:<5} {book[1][:24]:<25} {book[2][:19]:<20} {book[3]:<12} {book[4]:<12} {days_overdue:<12}\n"
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
