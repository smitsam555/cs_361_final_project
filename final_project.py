import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class GroceryApp:
    def __init__(self):
        self.item_list = ["Eggs (dozen)","Milk (gallons)", "Apples", "Cherries (lbs)", "Rice (lbs)", "Chicken (lbs)", "Bananas", "Cereal", "Ice Cream"]
        self.store_list = ["Quick Mart","Super Saver", "Corner Grocery", "Emporium", "Bob's Grocery"]

        self.root = tk.Tk()

        self.root.geometry("800x500")
        self.root.title("Grocery Price Comparison App")
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        self.app_name = tk.Label(self.root, text="Grocery Price Comparison App", font=('Arial', 18))
        self.app_name.pack()

        self.instructions = tk.Label(self.root, text="Instructions for this page...", font=('Arial', 12))
        self.instructions.pack()

        self.section_separator = tk.Frame(self.root)
        self.section_separator.columnconfigure(0, weight=1)
        self.section_separator.columnconfigure(1, weight=1)

        # SHOPPING LIST SECTION
        self.create_list = tk.Label(self.section_separator, text="Create Shopping List", font=('Arial', 16))
        self.create_list.grid(row=0, column=0, sticky=tk.W+tk.E, pady=5)

        self.item_select = ttk.Combobox(self.section_separator, state="readonly", values=self.item_list)
        self.item_select.grid(row=1, column=0, pady=5)

        self.item_btn_separator = tk.Frame(self.section_separator)

        self.add_item_btn = tk.Button(self.item_btn_separator, text="Add Item", font=("Arial", 10))
        self.add_item_btn.grid(row=0, column=0, padx=5)

        self.add_item_help = tk.Button(self.item_btn_separator, text="HELP", font=("Arial", 10), command=self.item_help)
        self.add_item_help.grid(row=0, column=1, padx=5)

        self.item_btn_separator.grid(row=2, column=0)

        self.item_table = tk.Frame(self.section_separator)

        self.item_head = tk.Label(self.item_table, text="Item", font=('Arial', 16))
        self.item_head.grid(row=0, column=0, padx=20)
        self.qty_head = tk.Label(self.item_table, text="Qty", font=('Arial', 16))
        self.qty_head.grid(row=0, column=1, padx=20)

        self.item_1 = tk.Label(self.item_table, text="Eggs (dozen)", font=('Arial', 14))
        self.item_1.grid(row=1, column=0, padx=20)
        self.qty_1 = tk.Label(self.item_table, text="2", font=('Arial', 14))
        self.qty_1.grid(row=1, column=1, padx=20)
        self.del_btn_1 = tk.Button(self.item_table, text="delete", font=('Arial', 10))
        self.del_btn_1.grid(row=1, column=2)

        self.item_2 = tk.Label(self.item_table, text="Milk (gallons)", font=('Arial', 14))
        self.item_2.grid(row=2, column=0, padx=20)
        self.qty_2 = tk.Label(self.item_table, text="1", font=('Arial', 14))
        self.qty_2.grid(row=2, column=1, padx=20)
        self.del_btn_2 = tk.Button(self.item_table, text="delete", font=('Arial', 10))
        self.del_btn_2.grid(row=2, column=2)

        self.item_3 = tk.Label(self.item_table, text="Apples", font=('Arial', 14))
        self.item_3.grid(row=3, column=0, padx=20)
        self.qty_3 = tk.Label(self.item_table, text="5", font=('Arial', 14))
        self.qty_3.grid(row=3, column=1, padx=20)
        self.del_btn_3 = tk.Button(self.item_table, text="delete", font=('Arial', 10))
        self.del_btn_3.grid(row=3, column=2)

        self.item_4 = tk.Label(self.item_table, text="Cherries (lbs)", font=('Arial', 14))
        self.item_4.grid(row=4, column=0, padx=20)
        self.qty_4 = tk.Label(self.item_table, text="0.5", font=('Arial', 14))
        self.qty_4.grid(row=4, column=1, padx=20)
        self.del_btn_4 = tk.Button(self.item_table, text="delete", font=('Arial', 10))
        self.del_btn_4.grid(row=4, column=2)

        self.item_5 = tk.Label(self.item_table, text="Rice (lbs)", font=('Arial', 14))
        self.item_5.grid(row=5, column=0, padx=20)
        self.qty_5 = tk.Label(self.item_table, text="4", font=('Arial', 14))
        self.qty_5.grid(row=5, column=1, padx=20)
        self.del_btn_5 = tk.Button(self.item_table, text="delete", font=('Arial', 10))
        self.del_btn_5.grid(row=5, column=2)

        self.item_table.grid(row=3, column=0, pady=15)


        # STORES SECTION
        self.choose_stores = tk.Label(self.section_separator, text="Choose Stores", font=('Arial', 16))
        self.choose_stores.grid(row=0, column=1, sticky=tk.W+tk.E)

        self.store_select = ttk.Combobox(self.section_separator, state="readonly", values=self.store_list)
        self.store_select.grid(row=1, column=1, pady=5)

        self.store_btn_separator = tk.Frame(self.section_separator)

        self.add_store_btn = tk.Button(self.store_btn_separator, text="Add Store", font=("Arial", 10))
        self.add_store_btn.grid(row=0, column=0, padx=5)

        self.add_store_help = tk.Button(self.store_btn_separator, text="HELP", font=("Arial", 10), command=self.store_help)
        self.add_store_help.grid(row=0, column=1, padx=5)

        self.store_btn_separator.grid(row=2, column=1)


        self.store_table = tk.Frame(self.section_separator)


        self.store_1_label = tk.Label(self.store_table, text="Store 1:", font=('Arial', 14))
        self.store_1_label.grid(row=0, column=0, padx=20)
        self.store_1 = tk.Label(self.store_table, text="Emporium", font=('Arial', 14))
        self.store_1.grid(row=0, column=1, padx=20)
        self.del_str_btn_1 = tk.Button(self.store_table, text="delete", font=('Arial', 10))
        self.del_str_btn_1.grid(row=0, column=2)

        self.store_2_label = tk.Label(self.store_table, text="Store 2:", font=('Arial', 14))
        self.store_2_label.grid(row=1, column=0, padx=20)
        self.store_2 = tk.Label(self.store_table, text="Bob's Grocery", font=('Arial', 14))
        self.store_2.grid(row=1, column=1, padx=20)
        self.del_str_btn_2 = tk.Button(self.store_table, text="delete", font=('Arial', 10))
        self.del_str_btn_2.grid(row=1, column=2)


        self.store_table.grid(row=3, column=1)

        self.section_separator.pack(pady=20)

        self.compare_btn = tk.Button(self.root, text="Compare List", font=("Arial", 16), command=self.compare)
        self.compare_btn.pack(pady=5)

        self.root.mainloop()

    def item_help(self):
        #print("need help adding items")
        messagebox.showinfo(title="Add Item Help",
                            message="To add an item, select it from the dropdown and click Add Item")


    def store_help(self):
        #print("need help choosing stores")
        messagebox.showinfo(title="Choose Store Help",
                            message="To choose a store, select it from the dropdown and click Add Store")

    def compare(self):
        #print("need help choosing stores")
        if messagebox.askyesno(title="Compare Prices?", message="Is your grocery list complete?"):
            self.root.destroy()
            self.root2 = tk.Tk()
            self.root2.geometry("800x500")
            self.root2.title("Grocery Price Comparison App")
            new_page = tk.Label(self.root2, text="Welcome to a New Page!", font=('Arial', 18))
            new_page.pack()
        #messagebox.showinfo(title="Compare Prices?",
        #                    message="Is your grocery list complete?")

    def close_window(self):
        if messagebox.askyesno(title="Exit Program?", message="Do you really want to exit the program?"):
            self.root.destroy()



GroceryApp()