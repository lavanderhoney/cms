import tkinter as tk
from tkinter import messagebox
import re
import csv
class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.left = None
        self.right = None


class CMS:
    def __init__(self):
        self.root = None

    def insert(self, root, contact_node):
        if root is None:
            return contact_node

        if contact_node.name < root.name:
            root.left = self.insert(root.left, contact_node)
        elif contact_node.name > root.name:
            root.right = self.insert(root.right, contact_node)

        return root

    def add_contact(self, name, phone, email):
        contact_node = Contact(name, phone, email)
        self.root = self.insert(self.root, contact_node)

    def search_by_name(self, root, find_name):
        if root is None or find_name in root.name:
            return root

        if find_name > root.name:
            return self.search_by_name(root.right, find_name)
        elif find_name < root.name:
            return self.search_by_name(root.left, find_name)

    def search_contact_by_name(self, name):
        return self.search_by_name(self.root, name)

    def search_by_phone(self, root, find_phone):
        if root is None or root.phone == find_phone:
            return root

        contacts = self.list_contacts()
        for contact in contacts:
            if contact.phone == find_phone:
                return contact

    def search_contact_by_phone(self, phone):
        return self.search_by_phone(self.root, phone)

    def update_contact(self, name, new_phone, new_email):
        node = self.search_contact_by_name(name)
        if node:
            node.phone = new_phone
            node.email = new_email

    def inorder_traversal(self, node, sequence):
        if node is not None:
            self.inorder_traversal(node.left, sequence)
            sequence.append(node)
            self.inorder_traversal(node.right, sequence)

    def list_contacts(self):
        sequence = []
        self.inorder_traversal(self.root, sequence)
        return sequence


def add_contact_button_click():
    name = name_entry.get().split(",")
    phone = phone_entry.get().split(",")
    email = email_entry.get().split(",")

    # name_pattern = r"^[A-Za-z\s]+$"  # Allow only letters and spaces
    phone_pattern = re.compile(r"^\d{10}$" ) # Allow exactly 10 digits
    email_pattern = r"^\S+@\S+\.\S+$"
    for n, p, e in zip(name, phone, email):
        if n and p and e:
            if re.fullmatch(phone_pattern, p) and re.fullmatch(email_pattern, e):
                cms.add_contact(n, p, e)

            elif not re.match(phone_pattern, p):
                messagebox.showerror("Error", "Invalid phone.")
                break
            elif not re.match(email_pattern, e):
                messagebox.showerror("Error", "Invalid email.")
                break
            else:
                messagebox.showerror("Error", "Invalid input. Please check all the fields.")
                break
        else:
            messagebox.showerror("Error","Enter all the fields")
    else:
        messagebox.showinfo("Success", "Contact added successfully.")
    name_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')
    email_entry.delete(0, 'end')


def search_contact_button_click():
    name = search_name_entry.get()
    name_pattern = r"^[A-Za-z\s]+$"  # Allow only letters and spaces

    if re.match(name_pattern, name):
        contact = cms.search_contact_by_name(name)
        if contact:
            display_search_result(contact)
        else:
            messagebox.showinfo("Search Result", "Contact not found.")
    else:
        messagebox.showerror("Error", "Enter correct name.")

    search_name_entry.delete(first=0, last='end')


def search_contact_phone_button_click():
    phone_pattern = re.compile(r"^\d{10}$" )  # Allow exactly 10 digits
    phone = search_phone_entry.get()
    if re.match(phone_pattern, phone):
        contact = cms.search_contact_by_phone(phone)
        if contact:
            display_search_result(contact)
        else:
            messagebox.showinfo("Search Result", "Contact not found.")
    else:
        messagebox.showerror("Error", "Enter valid phone number.")

    search_name_entry.delete(first=0, last='end')


def update_contact_button_click():
    name = update_name_entry.get()
    new_phone = new_phone_entry.get()
    new_email = new_email_entry.get()
    contact = cms.search_contact_by_name(name)
    if contact:
        if name and new_phone:
            if new_email:
                cms.update_contact(name, new_phone, new_email)
                messagebox.showinfo("Success", "Contact updated successfully.")
                update_name_entry.delete(0, 'end')
                new_phone_entry.delete(0, 'end')
                new_email_entry.delete(0, 'end')
            else:
                messagebox.showerror("Error", "All fields are required.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    else:
        messagebox.showerror("Error","Contact not found")

def save_to_file_button_click():
    contacts = cms.list_contacts()

    # Write all contacts to the CSV file
    with open('contacts.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for contact in contacts:
            if contact.name and contact.phone and contact.email:
                writer.writerow([contact.name, contact.phone, contact.email])
            else:
                messagebox.showerror("Error","Can't save blank file")
                break

    messagebox.showinfo("Success", "Contacts saved to file successfully.")


def create_styled_toplevel(title, width, height):
    top = tk.Toplevel(root)
    top.title(title)
    top.geometry(f"{width}x{height}")
    top.configure(bg="lightblue")
    return top

def display_search_result(contact):
    search_result_window = create_styled_toplevel("Search Result", 250, 550)
    search_result_window.title("Search Result")
    # search_result_window.geometry("600x600")
    window_frame = tk.Frame(search_result_window)
    result_text = f"Name: {contact.name}\nPhone: {contact.phone}\nEmail: {contact.email}"
    search_label = tk.Label
    result_label = tk.Label(window_frame, text=result_text,font=default_font)
    result_label.pack()
    window_frame.pack()


def traverse_button_click():
    contacts = cms.list_contacts()
    contact_list_window = create_styled_toplevel("Search Result", 250, 550)
    contact_list_window.title("List of all the contacts")
    # contact_list_window.geometry("400x400")

    for contact in contacts:
        contact_text = f"Name: {contact.name}\nPhone: {contact.phone}\nEmail: {contact.email}"
        contact_frame = tk.Frame(contact_list_window)
        contact_frame.pack(pady=7)
        contact_label = tk.Label(contact_frame, text=contact_text,font=default_font)
        contact_label.pack()


# Create CMS object
cms = CMS()

# Create the main window
root = tk.Tk()
root.title("Contact Management System")
root.geometry("1000x400")
root.minsize(900,370)
root.maxsize(1100,500)

default_font = ("Century", 11)

# Title Label
title_label = tk.Label(root, text="Contact Management System", font=("Century", 20,"bold"))
title_label.pack(side="top", pady=10,anchor="n")

main_frame =tk.Frame(root, pady=5,padx=5)
# Add Contact
add_contact_frame = tk.Frame(main_frame, bd=2, relief="sunken", bg="white", padx=5, pady=5)
add_contact_frame.pack(side="left", padx=10, pady=10, fill="y")

name_label = tk.Label(add_contact_frame, text="Name:", font=default_font)
name_label.pack()
name_entry = tk.Entry(add_contact_frame, width=30, font=default_font)
name_entry.pack()

phone_label = tk.Label(add_contact_frame, text="Phone:", font=default_font)
phone_label.pack()
phone_entry = tk.Entry(add_contact_frame, width=30, font=default_font)
phone_entry.pack()
email_label = tk.Label(add_contact_frame, text="Email:", font=default_font)
email_label.pack()
email_entry = tk.Entry(add_contact_frame, width=30, font=default_font)
email_entry.pack()
add_contact_button = tk.Button(add_contact_frame, text="Add Contact", command=add_contact_button_click, font=default_font)
add_contact_button.pack(pady=5)

# Search Contact
search_contact_frame = tk.Frame(main_frame, bd=2, relief="sunken", bg="white", padx=5, pady=5)
search_contact_frame.pack(side="left", padx=10, pady=10, fill="y")

search_name_label = tk.Label(search_contact_frame, text="Search by Name:", font=default_font)
search_name_label.pack()
search_name_entry = tk.Entry(search_contact_frame, width=30, font=default_font)
search_name_entry.pack()
search_contact_button = tk.Button(search_contact_frame, text="Search", command=search_contact_button_click,
                                 font=default_font)
search_contact_button.pack(pady=5)
search_phone_label = tk.Label(search_contact_frame, text="Search by Phone:", font=default_font)
search_phone_label.pack()
search_phone_entry = tk.Entry(search_contact_frame, width=30, font=default_font)
search_phone_entry.pack()
search_contact_p_button = tk.Button(search_contact_frame, text="Search",
                                    command=search_contact_phone_button_click, font=default_font)
search_contact_p_button.pack(pady=0)

# Update Contact
update_contact_frame = tk.Frame(main_frame, bd=2, relief="sunken", bg="white", padx=10, pady=5)
update_contact_frame.pack(side="left", padx=10, pady=10, fill="y")

update_name_label = tk.Label(update_contact_frame, text="Update by Name:", font=default_font)
update_name_label.pack()
update_name_entry = tk.Entry(update_contact_frame, width=30, font=default_font)
update_name_entry.pack()
new_phone_label = tk.Label(update_contact_frame, text="New Phone:", font=default_font)
new_phone_label.pack()
new_phone_entry = tk.Entry(update_contact_frame, width=30, font=default_font)
new_phone_entry.pack()
new_email_label = tk.Label(update_contact_frame, text="New Email:", font=default_font)
new_email_label.pack()
new_email_entry = tk.Entry(update_contact_frame, width=30, font=default_font)
new_email_entry.pack()
update_contact_button = tk.Button(update_contact_frame, text="Update Contact", command=update_contact_button_click,
                                 font=default_font)
update_contact_button.pack(pady=10)

main_frame.pack()


# "See all contacts" button
traversal_frame = tk.Frame(root, bd=1, relief="groove", bg="white", padx=5, pady=5)
traversal_frame.pack(padx=10, pady=5)

traverse_button = tk.Button(traversal_frame, text="See all contacts", command=traverse_button_click, font=default_font)
traverse_button.pack(side="left",padx=5)

save_to_file_button = tk.Button(traversal_frame, text="Save to File", command=save_to_file_button_click, font=default_font)
save_to_file_button.pack(side="left",padx=5,anchor="s",pady=5)

root.mainloop()