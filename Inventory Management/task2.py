import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT NOT NULL, 
                  quantity INTEGER NOT NULL, 
                  price REAL NOT NULL,
                  category TEXT,
                  description TEXT,
                  supplier TEXT)''')
    conn.commit()
    conn.close()

# Main Application Class
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Set window size and position
        window_width = 800
        window_height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Initialize database
        init_db()

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.configure(style="Main.TFrame")

        # Configure styles for colors
        style = ttk.Style()
        style.configure("Main.TFrame", background="#f0f0f0")  # Light gray frame
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#333333")  # White table with dark text

        # Updated Treeview headings with bright yellow background and dark text
        style.configure("Treeview.Heading", background="#FFEB3B", foreground="#000000", font=("Arial", 10, "bold"))  # Bright Yellow with Black text
        style.map("Treeview.Heading", background=[("active", "#FDD835")])  # Slightly darker yellow on hover

        # Treeview for displaying items
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Name", "Quantity", "Price", "Category", "Description", "Supplier"), show="headings", style="Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Supplier", text="Supplier")
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Quantity", width=100)
        self.tree.column("Price", width=100)
        self.tree.column("Category", width=100)
        self.tree.column("Description", width=200)
        self.tree.column("Supplier", width=100)
        self.tree.grid(row=0, column=0, columnspan=4, pady=10)

        # Buttons with tk.Button for direct color control
        tk.Button(self.main_frame, text="Add Item", command=self.add_item_window, bg="#4CAF50", fg="white", relief="flat", padx=10, pady=5).grid(row=1, column=0, pady=5)
        tk.Button(self.main_frame, text="Edit Item", command=self.edit_item_window, bg="#008CBA", fg="white", relief="flat", padx=10, pady=5).grid(row=1, column=1, pady=5)
        tk.Button(self.main_frame, text="Delete Item", command=self.delete_item, bg="#f44336", fg="white", relief="flat", padx=10, pady=5).grid(row=1, column=2, pady=5)
        tk.Button(self.main_frame, text="Refresh", command=self.load_items, bg="#555555", fg="white", relief="flat", padx=10, pady=5).grid(row=1, column=3, pady=5)

        # Load initial data
        self.load_items()

    def load_items(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM items")
        for row in c.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()

    def add_item_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Add Item")
        self.new_window.geometry("400x300")
        self.new_window.configure(bg="#f0f0f0")

        ttk.Label(self.new_window, text="Name:", background="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.new_window)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.new_window, text="Quantity:", background="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(self.new_window)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.new_window, text="Price:", background="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
        self.price_entry = ttk.Entry(self.new_window)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.new_window, text="Category:", background="#f0f0f0").grid(row=3, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.new_window)
        self.category_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.new_window, text="Description:", background="#f0f0f0").grid(row=4, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.new_window)
        self.description_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.new_window, text="Supplier:", background="#f0f0f0").grid(row=5, column=0, padx=5, pady=5)
        self.supplier_entry = ttk.Entry(self.new_window)
        self.supplier_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(self.new_window, text="Add", command=self.add_item, bg="#4CAF50", fg="white", relief="flat", padx=10, pady=5).grid(row=6, column=0, columnspan=2, pady=10)

    def add_item(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()
        supplier = self.supplier_entry.get()

        if not name or not quantity or not price or not category or not description or not supplier:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            if quantity < 0 or price < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer and Price a positive number!")
            return

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("INSERT INTO items (name, quantity, price, category, description, supplier) VALUES (?, ?, ?, ?, ?, ?)", 
                  (name, quantity, price, category, description, supplier))
        conn.commit()
        conn.close()

        self.load_items()
        self.new_window.destroy()
        messagebox.showinfo("Success", "Item added successfully!")

    def edit_item_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to edit!")
            return

        item = self.tree.item(selected[0])["values"]
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit Item")
        self.edit_window.geometry("400x300")
        self.edit_window.configure(bg="#f0f0f0")

        ttk.Label(self.edit_window, text="Name:", background="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.edit_name_entry = ttk.Entry(self.edit_window)
        self.edit_name_entry.insert(0, item[1])
        self.edit_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.edit_window, text="Quantity:", background="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.edit_quantity_entry = ttk.Entry(self.edit_window)
        self.edit_quantity_entry.insert(0, item[2])
        self.edit_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.edit_window, text="Price:", background="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
        self.edit_price_entry = ttk.Entry(self.edit_window)
        self.edit_price_entry.insert(0, item[3])
        self.edit_price_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.edit_window, text="Category:", background="#f0f0f0").grid(row=3, column=0, padx=5, pady=5)
        self.edit_category_entry = ttk.Entry(self.edit_window)
        self.edit_category_entry.insert(0, item[4])
        self.edit_category_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.edit_window, text="Description:", background="#f0f0f0").grid(row=4, column=0, padx=5, pady=5)
        self.edit_description_entry = ttk.Entry(self.edit_window)
        self.edit_description_entry.insert(0, item[5])
        self.edit_description_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.edit_window, text="Supplier:", background="#f0f0f0").grid(row=5, column=0, padx=5, pady=5)
        self.edit_supplier_entry = ttk.Entry(self.edit_window)
        self.edit_supplier_entry.insert(0, item[6])
        self.edit_supplier_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(self.edit_window, text="Update", command=lambda: self.update_item(item[0]), bg="#008CBA", fg="white", relief="flat", padx=10, pady=5).grid(row=6, column=0, columnspan=2, pady=10)

    def update_item(self, item_id):
        name = self.edit_name_entry.get()
        quantity = self.edit_quantity_entry.get()
        price = self.edit_price_entry.get()
        category = self.edit_category_entry.get()
        description = self.edit_description_entry.get()
        supplier = self.edit_supplier_entry.get()

        if not name or not quantity or not price or not category or not description or not supplier:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            if quantity < 0 or price < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer and Price a positive number!")
            return

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("UPDATE items SET name=?, quantity=?, price=?, category=?, description=?, supplier=? WHERE id=?", 
                  (name, quantity, price, category, description, supplier, item_id))
        conn.commit()
        conn.close()

        self.load_items()
        self.edit_window.destroy()
        messagebox.showinfo("Success", "Item updated successfully!")

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to delete!")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            item_id = self.tree.item(selected[0])["values"][0]
            conn = sqlite3.connect('inventory.db')
            c = conn.cursor()
            c.execute("DELETE FROM items WHERE id=?", (item_id,))
            conn.commit()
            conn.close()
            self.load_items()
            messagebox.showinfo("Success", "Item deleted successfully!")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()