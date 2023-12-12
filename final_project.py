import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import json

HOST = "127.0.0.1"
PORT = 15153


class GroceryApp:
    def __init__(self):

        # Get Item List from Microservice
        self.item_list = list(self.get_store_items("Bob's Grocery").keys())
        self.store_list = ["Quick Mart", "Super Saver", "Corner Grocery", "Emporium", "Bob's Grocery"]

        # Set to EMPTY for final submission
        #self.grocery_list = [['eggs (dozen)', 1], ['milk (gallon)', 1], ['apples', 4], ['cherries (pounds)', 1.5], ['rice (pounds)', 5]]
        self.grocery_list = []

        self.root = tk.Tk()

        self.root.geometry("900x900")
        self.root.title("Grocery Price Comparison App")
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        self.main_page = tk.Frame(self.root)

        self.app_name = tk.Label(self.main_page, text="Grocery Price Comparison App", font=('Arial', 28))
        self.app_name.pack(pady=10)

        # INSTRUCTIONS
        self.show_instructions()

        self.section_separator = tk.Frame(self.main_page)
        self.section_separator.columnconfigure(0, weight=1)
        self.section_separator.columnconfigure(1, weight=1)

        # SHOPPING LIST SECTION
        self.build_list_section()

        # ITEM TABLE
        self.build_item_table()

        # STORES SECTION
        self.build_store_section()

        self.compare_btn = tk.Button(self.section_separator, text="Compare List", font=("Arial", 24), command=self.compare, background='#A7A6BA')
        self.compare_btn.grid(row=3, column=1, padx=30, pady=30)

        self.section_separator.pack(pady=20)

        self.main_page.pack()

        self.root.mainloop()


    def item_help(self):
        """Displays help for adding items"""
        messagebox.showinfo(title="Add Item Help",
                            message="To add an item, select it from the dropdown, choose a quantity and click Add Item")


    def store_help(self):
        """Displays help for selecting stores and viewing prices"""
        messagebox.showinfo(title="Choose Store Help",
                            message="To choose a store, select it from the dropdown. \nIf you would like to see all prices for a store, click Get Store Prices")


    def show_instructions(self):
        """Displays App instructions on main page"""
        self.instructions_1 = tk.Label(self.main_page,
                                       text="Instructions: Create a Grocery List below, then select your favorite stores and click",
                                       font=('Arial', 12))
        self.instructions_1.pack()
        self.instructions_2 = tk.Label(self.main_page,
                                       text="'Compare List' to see which store has the best prices for your list!",
                                       font=('Arial', 12))
        self.instructions_2.pack()


    def build_list_section(self):
        """Displays selections and buttons for Grocery List section of App"""

        self.create_list = tk.Label(self.section_separator, text="Create Shopping List", font=('Arial', 16))
        self.create_list.grid(row=0, column=0, sticky=tk.W + tk.E, pady=5)

        self.add_item_separator = tk.Frame(self.section_separator)

        self.add_item_label = tk.Label(self.add_item_separator, text="Select Item:", font=('Arial', 12))
        self.add_item_label.grid(row=0, column=0, padx=10, pady=5)
        self.qty_label = tk.Label(self.add_item_separator, text="Quantity:", font=('Arial', 12))
        self.qty_label.grid(row=0, column=1, padx=10, pady=5)

        self.item_select = ttk.Combobox(self.add_item_separator, state="readonly", values=self.item_list)
        self.item_select.grid(row=1, column=0, pady=5)

        self.qty_spin = ttk.Spinbox(self.add_item_separator, from_=0, to=10, width=5, font=('Arial', 10))
        self.qty_spin.grid(row=1, column=1, padx=5, pady=5)

        self.add_item_btn = tk.Button(self.add_item_separator, text="     Add Item     ", font=("Arial", 10), command=self.add_item)
        self.add_item_btn.grid(row=2, column=0, padx=5, pady=5)

        self.add_item_help = tk.Button(self.add_item_separator, text="HELP", font=("Arial", 10), command=self.item_help)
        self.add_item_help.grid(row=2, column=1, padx=5, pady=5)

        self.add_item_separator.grid(row=1, column=0)


    def build_item_table(self):
        """Displays table for building Grocery List"""

        self.item_table = tk.Frame(self.section_separator)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14))
        style.configure("Treeview", font=(None, 12), rowheight=25)

        self.table = ttk.Treeview(self.item_table, columns=('items', 'quantity'), show='headings', selectmode=tk.BROWSE)

        self.table.heading('items', text="Items")
        self.table.heading('quantity', text="Qty")
        self.table.column('quantity', anchor='center')
        self.table.pack()

        for el in range(len(self.grocery_list)):
            self.table.insert(parent="", index=tk.END, values=(self.grocery_list[el][0], self.grocery_list[el][1]))


        modify_list_separator = tk.Frame(self.item_table)
        edit_button = tk.Button(modify_list_separator, text="Edit Item", font=("Arial", 10), command=self.edit_list_item)
        edit_button.grid(row=0, column=0, padx=5)
        delete_button = tk.Button(modify_list_separator, text="Delete Item", font=("Arial", 10), command=self.delete_list_item)
        delete_button.grid(row=0, column=1, padx=5)

        modify_list_separator.pack(pady=10)

        modify_qty_separator = tk.Frame(self.item_table)
        self.item_to_edit = tk.Label(modify_qty_separator, text='', font=('Arial', 12))
        self.item_to_edit.grid(row=0, column=0, padx=5)
        self.qty_to_edit = tk.Entry(modify_qty_separator, font=('Arial', 12), state=tk.DISABLED)
        self.qty_to_edit.grid(row=0, column=1, padx=5)
        self.confirm_button = tk.Button(modify_qty_separator, text="Update", font=("Arial", 10), state=tk.DISABLED, command=self.update_qty)
        self.confirm_button.grid(row=0, column=2, padx=5)

        modify_qty_separator.pack(pady=10)

        self.item_table.grid(row=3, column=0, pady=15)


    def build_store_section(self):
        """Displays selections and buttons for Store selection section of App"""

        self.choose_stores = tk.Label(self.section_separator, text="Choose Stores", font=('Arial', 16))
        self.choose_stores.grid(row=0, column=1, sticky=tk.W + tk.E)

        self.store_separator = tk.Frame(self.section_separator)

        self.store_1_label = tk.Label(self.store_separator, text="Store 1:", font=('Arial', 12))
        self.store_1_label.grid(row=0, column=0, padx=10, pady=5)
        self.store_2_label = tk.Label(self.store_separator, text="Store 2:", font=('Arial', 12))
        self.store_2_label.grid(row=0, column=1, padx=10, pady=5)

        self.store_1 = ttk.Combobox(self.store_separator, state="readonly", values=self.store_list)
        self.store_1.grid(row=1, column=0, padx=10, pady=5)
        self.get_prices_1 = tk.Button(self.store_separator, text="Get Store 1 Prices", font=("Arial", 10), command=lambda: self.price_list(self.store_1.get()))
        self.get_prices_1.grid(row=2, column=0, pady=5)

        self.store_2 = ttk.Combobox(self.store_separator, state="readonly", values=self.store_list)
        self.store_2.grid(row=1, column=1, padx=10, pady=5)
        self.get_prices_2 = tk.Button(self.store_separator, text="Get Store 2 Prices", font=("Arial", 10), command=lambda: self.price_list(self.store_2.get()))
        self.get_prices_2.grid(row=2, column=1, pady=5)

        self.add_store_help = tk.Button(self.store_separator, text="HELP", font=("Arial", 10), command=self.store_help)
        self.add_store_help.grid(row=2, column=2, pady=5)

        self.store_separator.grid(row=1, column=1)



    def edit_list_item(self):
        """Allows user to edit an item from the Grocery List"""
        selected_item = self.table.focus()
        item_name = self.table.item(selected_item)['values'][0]
        item_qty = self.table.item(selected_item)['values'][1]
        self.item_to_edit.config(text=item_name)
        self.qty_to_edit.config(state=tk.NORMAL)
        self.qty_to_edit.insert(0, item_qty)
        self.confirm_button.config(state=tk.NORMAL)



    def update_qty(self):
        """Allows user to update the quantity of an item in the Grocery List"""
        item_name = self.item_to_edit['text']
        item_qty = self.qty_to_edit.get()

        index = 0
        while self.grocery_list[index][0] != item_name:
            index += 1
        self.grocery_list[index][1] = item_qty
        selected_item = self.table.focus()
        self.table.item(selected_item, text='', values=(item_name, item_qty))
        self.item_to_edit.config(text='')
        self.qty_to_edit.delete(0, tk.END)
        self.qty_to_edit.config(state=tk.DISABLED)
        self.confirm_button.config(state=tk.DISABLED)
        if float(item_qty) == 0:
            self.delete_list_item()



    def delete_list_item(self):
        """Allows user to delete an item from the Grocery List"""
        selected_item = self.table.focus()
        item_name = self.table.item(selected_item)['values'][0]

        index = 0
        while self.grocery_list[index][0] != item_name:
            index +=1
        del self.grocery_list[index]
        self.table.delete(selected_item)



    def add_item(self):
        """Allows user to add an item to the Grocery List"""
        new_item = self.item_select.get()
        new_qty = self.qty_spin.get()
        self.grocery_list.append([new_item, new_qty])
        self.item_table.forget()
        self.build_item_table()
        self.item_select.set('')
        self.qty_spin.set('')


    def get_store_items(self, store_choice):
        """Calls microservice to receive grocery item list and pricing"""

        store_dict = {"Bob's Grocery": '1', "Quick Mart": '2', "Super Saver": '3'}

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to server
        client_socket.connect((HOST, PORT))

        choice = store_dict[store_choice]
        # send client choice to server
        client_socket.sendall(choice.encode('utf-8'))

        # receive JSON data from server
        data = client_socket.recv(1024).decode('utf-8')
        item_dict = json.loads(data)

        client_socket.close()

        return item_dict


    def price_list(self, selected_store):
        """Displays all items and prices for the selected store"""

        item_dict = self.get_store_items(selected_store)
        item_from_dict = list(item_dict.keys())
        price_from_dict = list(item_dict.values())

        if messagebox.askyesno(title="See Store Prices?", message="Would you like to see prices for this store?"):
            self.main_page.forget()
            self.prices_page = tk.Frame(self.root)

            results = tk.Label(self.prices_page, text=selected_store + " Price List", font=('Arial', 18))
            results.pack(pady=20)

            item_table = tk.Frame(self.prices_page)

            item_head = tk.Label(item_table, text="Item", font=('Arial', 16))
            item_head.grid(row=0, column=0, padx=20)
            qty_head = tk.Label(item_table, text="Price", font=('Arial', 16))
            qty_head.grid(row=0, column=1, padx=20)

            for item in range(len(item_from_dict)):
                store_item = tk.Label(item_table, text=item_from_dict[item], font=('Arial', 14))
                store_item.grid(row=item + 1, column=0, padx=20)
                price = tk.Label(item_table, text='${:,.2f}'.format(price_from_dict[item]), font=('Arial', 14))
                price.grid(row=item + 1, column=1, padx=20)

            item_table.pack()

            back_btn = tk.Button(self.prices_page, text="Back to Shopping List", font=('Arial', 16), command=self.back_to_start_prices)
            back_btn.pack(pady=20)

            self.prices_page.pack()


    def compare(self):
        """Calculates and displays best price information based on Grocery List and selected stores"""

        if messagebox.askyesno(title="Compare Prices?", message="Is your grocery list complete?"):
            self.main_page.forget()
            self.results_page = tk.Frame(self.root)

            results = tk.Label(self.results_page, text="Price Comparison Results", font=('Arial', 18))
            results.pack(pady=20)

            store1_prices = self.get_store_items(self.store_1.get())
            store2_prices = self.get_store_items(self.store_2.get())

            store1_total = 0
            store2_total = 0

            for item in self.grocery_list:
                store1_total += float(item[1]) * store1_prices[item[0]]
                store2_total += float(item[1]) * store2_prices[item[0]]

            if store1_total > store2_total:
                cheapest = self.store_2.get()
                total_price = round(store2_total, 2)
                savings = round(store1_total - store2_total, 2)
            elif store2_total > store1_total:
                cheapest = self.store_1.get()
                total_price = round(store1_total, 2)
                savings = round(store2_total - store1_total, 2)
            else:
                cheapest = 'Both are Equal'
                total_price = round(store2_total, 2)
                savings = round(store1_total - store2_total, 2)

            best_store = tk.Label(self.results_page, text="Cheapest Store: " + cheapest, font=('Arial', 16))
            best_store.pack(pady=15)

            total_price = tk.Label(self.results_page, text="Your total price: $" + str(total_price), font=('Arial', 16))
            total_price.pack(pady=10)

            savings = tk.Label(self.results_page, text="Your savings: $" + str(savings), font=('Arial', 16))
            savings.pack(pady=10)

            back_btn = tk.Button(self.results_page, text="Back to Shopping List", font=('Arial', 16), command=self.back_to_start_results)
            back_btn.pack(pady=20)
            self.results_page.pack()



    def close_window(self):
        """Displays close window message box to user"""
        if messagebox.askyesno(title="Exit Program?", message="Do you really want to exit the program?"):
            self.root.destroy()


    def back_to_start_results(self):
        """Takes user back to main page from results page"""
        if messagebox.askyesno(title="Go Back?", message="Do you want to return to your shopping list?"):
            self.results_page.forget()
            self.main_page.pack()


    def back_to_start_prices(self):
        """Takes user back to main page from prices page"""
        if messagebox.askyesno(title="Go Back?", message="Do you want to return to your shopping list?"):
            self.prices_page.forget()
            self.main_page.pack()



GroceryApp()