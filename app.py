import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

#  MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["clothes_db"]
collection = db["items"]

#  Main Window
root = tk.Tk()
root.title("👕 Clothes Store")
root.geometry("600x550")
root.configure(bg="#f3e5f5")  # light purple background

#  Styling
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12, "bold"), padding=8)
style.map("TButton",
          background=[("active", "#7b1fa2")],  # purple on click
          foreground=[("active", "white")])

# Input Fields
tk.Label(root, text="Cloth Name:", font=("Helvetica", 12, "bold"), bg="#f3e5f5").pack(pady=5)
name_entry = ttk.Entry(root, width=35)
name_entry.pack(pady=5)

tk.Label(root, text="Price (₹):", font=("Helvetica", 12, "bold"), bg="#f3e5f5").pack(pady=5)
price_entry = ttk.Entry(root, width=35)
price_entry.pack(pady=5)

# ===== CRUD Functions =====
def create_item():
    """Add new cloth to MongoDB"""
    name = name_entry.get().strip()
    price = price_entry.get().strip()
    if name and price:
        try:
            price = float(price)
            collection.insert_one({"name": name, "price": price})
            messagebox.showinfo("✅ Success", f"{name} added successfully!")
            clear_inputs()
            read_items()
        except ValueError:
            messagebox.showerror("❌ Error", "Price must be a number!")
    else:
        messagebox.showerror("❌ Error", "Fill all fields!")

def read_items():
    """Display all clothes in table"""
    for row in tree.get_children():
        tree.delete(row)  # clear old rows

    items = collection.find()
    for item in items:
        tree.insert("", tk.END, values=(item["name"], f"₹{item['price']}"))

def update_item():
    """Update price of a cloth"""
    name = name_entry.get().strip()
    price = price_entry.get().strip()
    if name and price:
        try:
            price = float(price)
            result = collection.update_one({"name": name}, {"$set": {"price": price}})
            if result.matched_count > 0:
                messagebox.showinfo("✅ Updated", f"{name}'s price updated to ₹{price}")
                clear_inputs()
                read_items()
            else:
                messagebox.showwarning("⚠ Not Found", f"No cloth found with name '{name}'")
        except ValueError:
            messagebox.showerror("❌ Error", "Price must be a number!")
    else:
        messagebox.showerror("❌ Error", "Enter name and new price to update")

def delete_item():
    """Delete cloth from MongoDB"""
    name = name_entry.get().strip()
    if name:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            messagebox.showinfo("🗑 Deleted", f"{name} removed successfully!")
            clear_inputs()
            read_items()
        else:
            messagebox.showwarning("⚠ Not Found", f"No cloth found with name '{name}'")
    else:
        messagebox.showerror("❌ Error", "Enter name to delete")

def clear_inputs():
    """Clear input fields"""
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

#  Buttons
btn_frame = tk.Frame(root, bg="#f3e5f5")
btn_frame.pack(pady=20)

ttk.Button(btn_frame, text="👕 Add Cloth", command=create_item).grid(row=0, column=0, padx=10, pady=5)
ttk.Button(btn_frame, text="📜 View Clothes", command=read_items).grid(row=0, column=1, padx=10, pady=5)
ttk.Button(btn_frame, text="✏ Update Price", command=update_item).grid(row=1, column=0, padx=10, pady=5)
ttk.Button(btn_frame, text="❌ Delete Cloth", command=delete_item).grid(row=1, column=1, padx=10, pady=5)

# ===== Output Table =====
table_frame = tk.Frame(root, bg="#f3e5f5")
table_frame.pack(pady=10)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

columns = ("name", "price")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10, yscrollcommand=scrollbar.set)
tree.heading("name", text="Cloth Name")
tree.heading("price", text="Price (₹)")
tree.column("name", width=300, anchor="center")
tree.column("price", width=150, anchor="center")
tree.pack()

scrollbar.config(command=tree.yview)

# Run App
root.mainloop()
