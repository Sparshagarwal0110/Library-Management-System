# 📖 Overview

The Library Management System is a user-friendly desktop application that helps librarians efficiently manage book inventory, member registrations, and book circulation processes. It provides a complete solution for day-to-day library operations with an intuitive graphical interface.

# ✨ Features

**📚 Book Management**

Add New Books: Complete book details including title, author, ISBN, and quantity

View Book Catalog: Browse all books in the library with availability status

Delete Books: Remove books from inventory (with safety checks)

Inventory Tracking: Automatic tracking of available copies

**👥 Member Management**

Member Registration: Add new library members with contact information

Member Directory: View and manage all registered members

Membership Tracking: Record membership dates and details

**🔄 Circulation Management**

Book Issuing: Issue books to members with due dates

Book Returns: Process book returns efficiently

Borrowing Limits: Enforce maximum 5 books per member

Due Date Tracking: Automatic 14-day loan period calculation

**📊 Reporting System**
Books Report: Complete inventory listing

Members Report: Detailed member directory

Issued Books Report: Current circulation status

Overdue Books Report: Identify delayed returns

**🔧 Technical Details**

Built With
Python: Core programming language

Tkinter: GUI framework

SQLite: Database management

datetime: Date handling for due dates

Key Dependencies
Python Standard Library only - no external dependencies required

**🎯 Business Rules**

Maximum 5 books can be issued to a single member simultaneously

Standard loan period is 14 days

Books cannot be deleted if currently issued

Members cannot be deleted if they have issued books

ISBN and email addresses must be unique

Automatic availability tracking

**🚨 Error Handling**

The system includes comprehensive error handling for:

Duplicate ISBN/email entries

Invalid quantity values

Attempting to delete referenced records

Database integrity violations

Missing required fields

**📞 Contact**

Project Maintainer: Sparsh Agarwal
