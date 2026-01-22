##########################IMPORTED LIBRARIES###############################
import csv
import json
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##########################PREPERATION_CLASSES################################
# Define FILE to for convenience when calling
FILE = "/Users/gabrielsiallagan/Library/Mobile Documents/com~apple~CloudDocs/Desktop/IT assigment 2/users.csv"

#used to retrieve and update data in login and sign-up class
class UserManager:
    #function that is automatically called when creating the object
    def __init__(self):
        self.data = self.reader()
        print(self.data)
        #reads file into dictionary

    def login(self, username, password):
        return username in self.data and self.data[username] == password
        #return either 'true' or 'false' if user has an account and password is valid
    

    def signup(self, username, password):
        if username in self.data:
            return False
            #return false if user already has an account
        self.data[username] = password
        self.writer(self.data)
        #adds new account into csv file
        return True

    #main reader function that turns csv data into a dictionary
    def reader(self):
        data = {}
        with open(FILE, mode='r') as csvfile:
            reader = csv.reader(csvfile)
            #reader object
            data = dict((row[0], row[1]) for row in reader if len(row) >= 2)
            #creates the dictionary
        return data

    def writer(self, data):
        with open(FILE, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            #writer object
            for username, password in data.items():
                writer.writerow([username, password])
                #splits list variable into rows

class UserDataManager:
    def __init__(self, current_user):
        self.filepath = "/Users/gabrielsiallagan/Library/Mobile Documents/com~apple~CloudDocs/Desktop/IT assigment 2/" + current_user + "_data.json"
        self.data = self.load_data()
        #reads data

        # Subscribers for data changes
        self.subscribers = []

    #re-writes data according to updated data
    def save_data(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.data, file, indent=2)
        self.notify_subscribers()

    #set up dictionary with categories
    def initialize_month_expenses(self):
        """Initializes a dictionary for monthly expenses with categories."""
        return {
            "Food": [],
            "Rent": [],
            "Utilities": [],
            "Transportation": [],
            "Shopping": [],
            "Life and Entertainment": [],
            "Other": []
        }

    #get updated data and saves it into file
    def update_user_data(self, income, balance, savings_goal):
        """Updates user income, balance, and savings goal."""
        self.data["income"] = income
        self.data["balance"] = balance
        self.data["savings_goal"] = savings_goal
        self.save_data()

    #adds new expense with date and category into the file
    def add_expense(self, day, amount, category):
        """Adds an expense to a specific user for a given month."""
        if category in self.data["expenses"][str(day)]:
            self.data["expenses"][str(day)][category].append(amount)
        else:
            self.data["expenses"][str(day)][category] = [amount]
        self.save_data()

    #get total expense of each category for pie chart
    def get_category_expenses(self):
        """Calculates total expenses per category."""
        category_totals = {category: 0 for category in self.data["expenses"]["1"]}  # Initialize totals
        for day, categories in self.data["expenses"].items():
            for category, amounts in categories.items():
                category_totals[category] += sum(amounts)
        return category_totals
    #reads or creates file
    def load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                return json.load(file)
        else:
            return {
                "income": 0.0,
                "balance": 0.0,
                "savings_goal": 0.0,
                "expenses": {str(day): self.initialize_month_expenses() for day in range(1, 29)}
            }
    #calculates total expense
    def total_expense(self):
    
        categories = ["Food", "Rent", "Utilities", "Transportation", "Shopping", "Life and Entertainment", "Other"]

        # Initialize list to hold monthly expenses
        monthly_expense = []

        # Iterate over each day
        for day in range(1, 29):  # Use the actual range of days as integers
            day_str = str(day)    # Convert day to string to use as a key in the JSON data
            daily_expenses = []   # List to store daily expenses per category

            # Check if the day exists in the data
            for category in categories:
                # Check if the category exists for the day, and sum the expenses if it does
                category_sum = sum(self.data['expenses'][day_str].get(category, []))
                daily_expenses.append(category_sum)

            # Calculate the total expenses for the day
            daily_total = sum(daily_expenses)

            # Append daily total to monthly expenses
            monthly_expense.append(daily_total)
            total_monthly_expense = sum(monthly_expense)

        # Print the list of monthly expenses
        return total_monthly_expense

    def subscribe(self, callback):
        """Subscribe a callback to data changes."""
        self.subscribers.append(callback)
        ##This method allows other parts of the application to register a callback function that will be called whenever the data changes. A callback function is a piece of code that you want to run later in response to some event, such as a data update.



    def notify_subscribers(self):
        """Notify all subscribed components about data changes."""
        for callback in self.subscribers:
            callback()
        #This method is responsible for informing all subscribed components that the data has changed. When the data changes, this method will go through each subscribed callback and execute it, ensuring that every component is updated accordingly.

#to be called in login and signup to center window
class CenterWindow:
    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        ## The following lines of code were adapted from https://www.youtube.com/watch?v=TdTks2eSx3c&ab_channel=Codemy.com 

#class helps with the creation of frames
class Construction:
    #frame creation function
    def create_frame(self, parent, dimension, side, row=None, fill=None, expand=False):
        frame = Frame(parent, width=dimension[0], height=dimension[1], highlightbackground="#b09662", highlightthickness=2)
        frame.pack_propagate(False)  # Prevent the frame from resizing based on its content
        if row is None:
            frame.columnconfigure(0, weight=1)
            frame.pack(pady=10, side=side, fill=fill, expand=expand)
        else:
            for x in range(row):
                frame.columnconfigure(x, weight=1)
            frame.pack(pady=10, side=side, fill=fill, expand=expand)
        return frame
    #creates a label and an entry side by side
    def create_label_entry_pair(self, parent, label_text, row, fontsize, show=None):
        label = Label(parent, text=label_text, font=('Arial', fontsize))
        label.grid(row=row, column=0, sticky=W+E)

        # Frame to contain both Entry and Button
        entry_button_frame = Frame(parent)
        entry_button_frame.grid(row=row, column=1, sticky=W+E)

        entry = Entry(entry_button_frame, font=('Arial', fontsize), show=show)
        entry.pack(side=LEFT, fill=X, expand=True)  # Use pack for entry in this frame

        return label, entry  # Return the entry widget for later use

    # Add 'window' parameter to specify the window to be centered
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        ## The following lines of code were adapted from https://www.youtube.com/watch?v=TdTks2eSx3c&ab_channel=Codemy.com 


####################################################################


###########################LOGIN_WINDOW#############################
class LOGIN(Tk, CenterWindow):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        self.title("Login/Signup")
        self.resizable(False, False)
        self.center_window(500, 200)
        self.create_widgets()
        self.mainloop()

    def create_widgets(self):
        self.create_input_frame()
        self.create_buttons()

    def create_input_frame(self):
        self.login_frame = Frame(self)
        self.login_frame.columnconfigure(0, weight=1)
        self.login_frame.columnconfigure(1, weight=1)
        self.login_frame.pack(padx=20, pady=(20, 0), fill=BOTH, expand=False)

        self.create_label_entry_pair(self.login_frame, "Username: ", 0)
        self.create_label_entry_pair(self.login_frame, "Password: ", 1, show='*')

    def create_label_entry_pair(self, parent, label_text, row, show=None):
        label = Label(parent, text=label_text, font=('Arial', 18))
        label.grid(row=row, column=0, sticky=W+E, pady=10)

        entry = Entry(parent, font=('Arial', 18), show=show)
        entry.grid(row=row, column=1, sticky=W+E, pady=10)

        if row == 0:
            self.entry_username = entry
        else:
            self.entry_password = entry

    def create_buttons(self):
        self.login_button = Button(self, text='Login', font=('Arial', 15), command=self.login)
        self.login_button.pack()

        self.signup_button = Button(self, text='Sign Up', font=('Arial', 15), command=self.open_signup_window)
        self.signup_button.pack()

    def login(self):
        username = self.entry_username.get().strip().lower()
        password = self.entry_password.get()
        if self.user_manager.login(username, password):
            messagebox.showinfo("Login", "Login Successful!")
            self.destroy()
            main_window = WINDOW(username)
            main_window.mainloop()
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    def open_signup_window(self):
        SignupWindow(self)
######################################################################


############################SIGN-UP_WINDOW############################
#toplevel used to create a window on top of a window
class SignupWindow(Toplevel, CenterWindow):
    def __init__(self, login_instance):
        super().__init__()
        self.login_instance = login_instance
        self.title("Sign Up")
        self.resizable(False, False)
        self.center_window(500, 200)
        self.create_widgets()

    #widgets within this window
    def create_widgets(self):
        self.signup_frame = Frame(self)
        self.signup_frame.columnconfigure(0, weight=1)
        self.signup_frame.columnconfigure(1, weight=1)
        self.signup_frame.pack(padx=20, pady=(20, 0), fill=BOTH, expand=False)

        self.create_label_entry_pair(self.signup_frame, "Username: ", 0)
        self.create_label_entry_pair(self.signup_frame, "Password: ", 1, show='*')

        self.signup_button = Button(self, text='Sign Up', font=('Arial', 15), command=self.signup)
        self.signup_button.pack()

    #creates a label and entry specific to login page
    def create_label_entry_pair(self, parent, label_text, row, show=None):
        label = Label(parent, text=label_text, font=('Arial', 18))  
        label.grid(row=row, column=0, sticky=W+E, pady=10)

        entry = Entry(parent, font=('Arial', 18), show=show)
        entry.grid(row=row, column=1, sticky=W+E, pady=10)

        if row == 0:
            self.entry_username = entry
        else:
            self.entry_password = entry

    #function for users to make an account
    def signup(self):
        username = self.entry_username.get().strip().lower()
        password = self.entry_password.get()
        if self.login_instance.user_manager.signup(username, password):
            messagebox.showinfo("Sign Up", "Sign Up Successful!")
            self.destroy()
        else:
            messagebox.showerror("Sign Up", "Username already exists.")
################################################################################

###########################MAIN_WINDOW_FRAMES###################################

#to be added in the main window class
class FrameRight(Construction):
    def __init__(self, parent, data_manager):
        self.data_manager = data_manager
        self.widget_frame_right = self.create_frame(parent, (300, 300), RIGHT, row=None, fill='y')
        self.widget_frame_right.configure(bg='#1c1d20')
        self.expense(self.widget_frame_right)

        # Subscribe to data changes
        self.data_manager.subscribe(self.update_table)#if there is a change in data from any other frame, table will update
    
    #expense widgets
    def expense(self, frame):
        Label(frame, text='Add Expense', fg = '#b09662', bg = '#421d59').grid(row=0, column=0, columnspan=2)
        self.expense_amount = self.create_label_entry_pair(frame, 'Amount:', 1, 13)
        self.expense_amount_label, self.expense_amount_entry = self.expense_amount
        self.expense_amount_label.configure(fg = '#b09662', bg = '#421d59')
        Label(frame, text="Date:", fg = '#b09662', bg = '#421d59').grid(row=2, column=0, sticky=W)
        self.expense_day = ttk.Combobox(frame, values=list(range(1, 29))) # More concise way to list days
        self.expense_day.grid(row=2, column=1)
        Label(frame, text="Category:", fg = '#b09662', bg = '#421d59').grid(row=3, column=0, sticky=W)
        self.expense_category = ttk.Combobox(frame, values=["Food", "Rent", "Utilities", "Transportation", "Shopping", "Life and Entertainment", "Other"])
        self.expense_category.grid(row=3, column=1)
        Button(frame, text="Add Expense", font=('Arial', 15), command=self.add_expense, highlightbackground='#b09662').grid(row=4, column=0, columnspan=2, pady=10)
        Button(frame, text="View Expense", font=('Arial', 15), command=self.expensepie, highlightbackground='#b09662').grid(row=5, column=0, columnspan=2, pady=10)
        self.Table(frame)

    #gets input from entries and adds to file
    def add_expense(self):
        try:
            # Validate inputs
            expense_amount = float(self.expense_amount[1].get())
            expense_day = int(self.expense_day.get())
            expense_category = self.expense_category.get()
            #error handling
            if expense_amount <= 0:
                messagebox.showerror("Invalid Input", "Please enter a postive amount.")
            else:

                # Update the data manager
                self.data_manager.add_expense(expense_day, expense_amount, expense_category)#add to file

                messagebox.showinfo("Success", "Expense added successfully.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for amount and day.")

    #piechart widget
    def expensepie(self):
        # Create a new Toplevel window
        pie_window = Toplevel(self.widget_frame_right) 
        pie_window.title("Expense Distribution")

        # Center the Toplevel window instead of the main window
        self.center_window(pie_window, 700, 500)

        # Create the pie chart
        fig, ax = plt.subplots()
        
        # Get the total expenses per category
        category_expenses = self.data_manager.get_category_expenses()
        categories = list(category_expenses.keys())
        amounts = list(category_expenses.values())
        
        ax.pie(amounts, labels=categories, textprops={'fontsize': 10}, autopct='%1.1f%%')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Monthly Expenses Distribution')

        # Create a canvas for the figure and add it to the Toplevel window
        canvas = FigureCanvasTkAgg(fig, master=pie_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        # Ensure that the window is closed properly
        pie_window.protocol("WM_DELETE_WINDOW", pie_window.destroy)

    #table widget
    def Table(self, frame):
        self.entry_frame = self.create_frame(frame, (500, 600), BOTTOM)
        self.tree = ttk.Treeview(self.entry_frame, columns=("Day", "category", "Amount"), show='headings', height = 40)

        # Define the column headings
        self.tree.heading("Day", text="Day")
        self.tree.heading("category", text="Category")
        self.tree.heading("Amount", text="Amount")

        # Define the column width
        self.tree.column("Day", width=50)
        self.tree.column("category", width=150)
        self.tree.column("Amount", width=50)
        


        # Add a scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(self.entry_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.table_data()
        for expense in self.all_expenses:
            day, category, amount = expense
            self.tree.insert("", END, values=(day, category, amount))


        self.tree.pack(side=TOP)

    #updates treeview table after every expense entry
    def update_table(self):
        """Refresh the expense table with current data."""
        # Clear existing entries in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get all expense data
        all_expenses = self.table_data()

        # Insert data into the table
        for expense in all_expenses:
            day, category, amount = expense
            self.tree.insert("", END, values=(day, category, amount))

    #to get data to insert into treeview table
    def table_data(self):
        categories = ["Food", "Rent", "Utilities", "Transportation", "Shopping", "Life and Entertainment", "Other"]
        days = list(self.data_manager.data['expenses'].keys())

        self.all_expenses = [
            [day, category, expense]
            for day in days
            for category in categories
            for expense in self.data_manager.data['expenses'][day][category]
        ]

        return self.all_expenses


#to be added in the main window class
class FrameLeft(Construction):
    def __init__(self, parent, data_manager):
        self.data_manager = data_manager
        self.widget_frame_left = self.create_frame(parent, (300, 300), LEFT, row=None, fill='y')
        self.widget_frame_left.configure(bg='#1c1d20')

        # Initialize the current values
        self.current_balance = data_manager.data["balance"]
        self.current_income = data_manager.data["income"]
        self.current_savings_goal = data_manager.data["savings_goal"]
        self.total_expense = self.data_manager.total_expense()
        self.new_balance = self.current_balance + self.current_income
        self.net_balance = self.new_balance - self.total_expense

        # Create Balance Entry and Button
        balance_label, self.balance_entry = self.create_label_entry_pair(self.widget_frame_left, "Balance", 0, 18)
        balance_label.configure(fg = '#b09662', bg = '#421d59')
        self.balance_button = Button(self.widget_frame_left, text="Update", font=('Arial', 15), command=self.update_balance, highlightbackground='#b09662')
        self.balance_button.grid(row=0, column=2, sticky=W, padx=(5, 0))

        # Create Income Entry and Button
        income_label, self.income_entry = self.create_label_entry_pair(self.widget_frame_left, "Income", 1, 18)
        income_label.configure(fg = '#b09662', bg = '#421d59')
        self.income_button = Button(self.widget_frame_left, text="Update", font=('Arial', 15), command=self.update_income, highlightbackground='#b09662')
        self.income_button.grid(row=1, column=2, sticky=W, padx=(5, 0))

        # Create Savings Goals Entry and Button
        savings_label, self.savings_entry = self.create_label_entry_pair(self.widget_frame_left, "Monthly Savings Goals", 2, 18)
        savings_label.configure(fg = '#b09662', bg = '#421d59')
        self.savings_button = Button(self.widget_frame_left, text="Update", font=('Arial', 15), command=self.update_savings, highlightbackground='#b09662')

        self.savings_button.grid(row=2, column=2, sticky=W, padx=(5, 0))


        # Create Display Labels for stats at the bottom of the frame
        self.balance_display = Label(self.widget_frame_left, text=f"Initial Balance: ${self.current_balance:.2f}", font=('Arial', 20), fg = '#14d368', bg = '#797d7f')
        self.balance_display.grid(row=3, column=0, columnspan=3, sticky=W, pady=(100, 15))

        self.income_display = Label(self.widget_frame_left, text=f"Current Income: ${self.current_income:.2f}", font=('Arial', 20), fg = '#1559d7', bg = '#797d7f')
        self.income_display.grid(row=4, column=0, columnspan=3, sticky=W, pady=15)

        self.new_balance_display = Label(self.widget_frame_left, text=f"Balance after Income: ${(self.new_balance):.2f}", font=('Arial', 20), fg = '#14d368', bg = '#797d7f')
        self.new_balance_display.grid(row=5, column=0, columnspan=3, sticky=W, pady=15)

        self.total_expense_display = Label(self.widget_frame_left, text=f"Total Expense: ${(self.total_expense):.2f}", font=('Arial', 20), fg = '#f00e29', bg = '#797d7f')
        self.total_expense_display.grid(row=6, column=0, columnspan=3, sticky=W, pady=15)

        self.net_balance_display = Label(self.widget_frame_left, text=f"Net Balance: ${(self.net_balance):.2f}", font=('Arial', 20), fg = '#14d368', bg = '#797d7f')
        self.net_balance_display.grid(row=7, column=0, columnspan=3, sticky=W, pady=15)

        self.savings_display = Label(self.widget_frame_left, text=f"Monthly Savings Goal: ${self.current_savings_goal:.2f}", font=('Arial', 20), fg = '#14d368', bg = '#797d7f')
        self.savings_display.grid(row=8, column=0, columnspan=3, sticky=W, pady=15)

        self.daily_savings_expense_display = Label(self.widget_frame_left, text=f"Daily Savings Expense: ${self.calculate_daily_savings_expense():.2f}", font=('Arial', 20), fg = '#14d368', bg = '#797d7f')
        self.daily_savings_expense_display.grid(row=9, column=0, columnspan=3, sticky=W, pady=15)

        #feasibility font colour is dependent on feasiblity it self
        if self.get_feasibility(self.calculate_daily_savings_expense()) == "Not Feasible":
            self.feasibility_display = Label(self.widget_frame_left, text=self.get_feasibility(self.calculate_daily_savings_expense()), font=('Arial', 20), fg = '#f00e29', bg = '#797d7f')
        elif self.get_feasibility(self.calculate_daily_savings_expense()) == "Possible but difficult":
            self.feasibility_display = Label(self.widget_frame_left, text=self.get_feasibility(self.calculate_daily_savings_expense()), font=('Arial', 20), fg = '#f27c1b', bg = '#797d7f')
        elif self.get_feasibility(self.calculate_daily_savings_expense()) == "Possible":
            self.feasibility_display = Label(self.widget_frame_left, text=self.get_feasibility(self.calculate_daily_savings_expense()), font=('Arial', 20), fg = '#14d368', bg = '#797d7f')
        self.feasibility_display.grid(row=10, column=0, columnspan=3, sticky=W, pady=15)

        # Subscribe to data changes
        self.data_manager.subscribe(self.update_frame)

    def calculate_daily_savings_expense(self):
        """Calculates the daily amount available after the savings goal is subtracted from the income."""
        #self.current_income and self.current_savings_goal cannot be 0 when calculating
        if self.current_income and self.current_savings_goal:
            return (self.current_income - self.current_savings_goal) / 28
        return 0.0

    #get balance input and updates file data and in UI
    def update_balance(self):
        """Updates the balance and reflects the changes in the UI."""
        #error handling
        try:
            balance_value = float(self.balance_entry.get())
            if balance_value <=0:
                messagebox.showerror("Invalid Input", "Please enter a positive number for balance.")
            else:
            
                self.current_balance = balance_value

                # Update the data manager
                self.data_manager.data["balance"] = self.current_balance
                self.data_manager.save_data()

                self.balance_display.config(text=f"Current Balance: ${self.current_balance:.2f}")
                self.update_displays()
                messagebox.showinfo("Update Successful", "Balance updated successfully.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for balance.")

    #get income input and updates file data and in UI
    def update_income(self):
        """Updates the income and reflects the changes in the UI."""
        try:
            income_value = float(self.income_entry.get())

            if income_value <=0:
                messagebox.showerror("Invalid Input", "Please enter a positive number for Income.")

            else:
                self.current_income = income_value

                # Update the data manager
                self.data_manager.data["income"] = self.current_income
                self.data_manager.save_data()

                self.income_display.config(text=f"Current Income: ${self.current_income:.2f}")
                self.update_displays()
                messagebox.showinfo("Update Successful", "Income updated successfully.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for income.")

    def update_savings(self):
        #Updates the savings goal and reflects the changes in the UI.
        try:
            savings_value = float(self.savings_entry.get())

            if savings_value <= 0:
                messagebox.showerror("Invalid Input", "Please enter a positive number for Savings Goal.")

            elif savings_value > self.current_income:
                messagebox.showerror("Invalid Input", "Savings Goal must be less than Income")
            else:
                self.current_savings_goal = savings_value

                # Update the data manager
                self.data_manager.data["savings_goal"] = self.current_savings_goal
                self.data_manager.save_data()

                self.savings_display.config(text=f"Monthly Savings Goal: ${self.current_savings_goal:.2f}")
                self.update_displays()
                messagebox.showinfo("Update Successful", "Savings Goal updated successfully.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for savings goal.")

    #updates widgets after change in data from within the window
    def update_displays(self):
        """Updates all display labels to reflect the current state."""
        # Calculate the new balance and net balance
        self.new_balance = self.current_balance + self.current_income
        self.total_expense = self.data_manager.total_expense()
        self.net_balance = self.new_balance - self.total_expense
        
        # Update display labels with new values
        self.new_balance_display.config(text=f"Balance after Income: ${self.new_balance:.2f}")
        self.total_expense_display.config(text=f"Total Expense: ${self.total_expense:.2f}")
        self.net_balance_display.config(text=f"Net Balance: ${self.net_balance:.2f}")

        # Update the daily savings expense
        daily_savings_expense = self.calculate_daily_savings_expense()
        self.daily_savings_expense_display.config(text=f"Daily Savings Expense: ${daily_savings_expense:.2f}")

        # Update feasibility display
        if self.get_feasibility(daily_savings_expense) == "Not Feasible":
            self.feasibility_display.config(text=self.get_feasibility(daily_savings_expense),fg = '#f00e29', bg = '#797d7f')
        elif self.get_feasibility(daily_savings_expense) == "Possible but difficult":
            self.feasibility_display.config(text=self.get_feasibility(daily_savings_expense),fg = '#f27c1b', bg = '#797d7f')
        elif self.get_feasibility(daily_savings_expense) == "Possible":
           self.feasibility_display.config(text=self.get_feasibility(daily_savings_expense), fg = '#14d368', bg = '#797d7f')

    #funciton to access the feasibility of saving goal
    def get_feasibility(self, daily_expense):
        """Determines the feasibility of saving based on daily expenses."""
        if daily_expense <= 10:
            return "Not Feasible"
        elif daily_expense <= 20:
            return "Possible but difficult"
        return "Possible"

    #updates frame if there is any change in data within the window
    def update_frame(self):
        """Callback to update the frame when data changes."""
        self.current_balance = self.data_manager.data["balance"]
        self.current_income = self.data_manager.data["income"]
        self.current_savings_goal = self.data_manager.data["savings_goal"]
        
        # Update displays to reflect any changes
        self.update_displays()

        # Update the balance, income, and savings goal displays
        self.balance_display.config(text=f"Current Balance: ${self.current_balance:.2f}")
        self.income_display.config(text=f"Current Income: ${self.current_income:.2f}")
        self.savings_display.config(text=f"Monthly Savings Goal: ${self.current_savings_goal:.2f}")

#to be added in the main window class
class GraphFrame(Construction):
    def __init__(self, parent, data_manager):
        self.data_manager = data_manager
        self.graph_frame = self.create_frame(parent, (750, 750), TOP)

        # Store references to the figure and canvas
        self.fig = None
        self.canvas = None

        # Subscribe to data changes
        self.data_manager.subscribe(self.update_graph)

        # Initial plot
        self.plot_graph(self.graph_frame)

    def plot_graph(self, frame):
        """Initializes and draws the graph with existing data."""
        # Initialize figure and axes
        self.fig, ax = plt.subplots(figsize = (4, 8))  # Adjust figsize as needed

        # Fetch existing data from the data manager
        self.days = list(range(1, 29))  # Assuming 28 days for simplicity
        self.numbers = self.get_monthly_balance(self.data_manager.data)

        # Retrieve income and savings goal
        income = self.data_manager.data['income']
        balance = (self.data_manager.data["balance"]) + income
        monthly_savings_goal = (self.data_manager.data["savings_goal"]) +(self.data_manager.data["balance"])

        # Distribute income and savings goal equally for visualization
        self.balance = [balance] * 28  # Distribute monthly income equally
        self.savings_goal = [monthly_savings_goal] * 28  # Distribute savings goal equally

        # Plot the initial data
        ax.plot(self.days, self.numbers, color='blue', linewidth=2, marker='o', markerfacecolor='blue', markersize=3, label='Net Balance')
        ax.plot(self.days, self.balance, color='green', linewidth=1, linestyle='dotted', label='Balance After Income')
        ax.plot(self.days, self.savings_goal, color='red', linewidth=1, linestyle='dotted', label='Savings Goal')

        # Set labels and title
        ax.set_xlabel('Days')
        ax.set_ylabel('Balance ($)')
        ax.set_ylim(bottom=0)
        ax.set_title('Balance Graph')
        ax.legend(loc='upper right', fontsize = 10)  # Add legend

        # Adjust ticks
        ax.tick_params(axis='both', which='major', labelsize=10)  # Adjust the labelsize as needed

        

        # Create canvas for the figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=X, expand=False)

    #updates graph according to new set of data
    def update_graph(self):
        """Updates the graph with new data when notified of data changes."""
        # If the figure exists, clear the axes
        if self.fig:
            self.fig.clear()

            # Create new axes
            ax = self.fig.add_subplot(111)

            # Retrieve updated data
            self.days = list(range(1, 29))  # Assuming 28 days for simplicity
            self.numbers = self.get_monthly_balance(self.data_manager.data)

            # Update income and savings goal for visualization
            monthly_income = self.data_manager.data["income"]
            monthly_savings_goal = self.data_manager.data["savings_goal"] + (self.data_manager.data["balance"])
            self.income = [monthly_income] * 28  # Distribute monthly income equally
            self.savings_goal = [monthly_savings_goal] * 28  # Distribute savings goal equally

            # Plot the updated data
            ax.plot(self.days, self.numbers, color='blue', linewidth=2, marker='o', markerfacecolor='blue', markersize=3, label='Expenses')
            ax.plot(self.days, self.income, color='green', linewidth=1, linestyle='dotted', label='Income')
            ax.plot(self.days, self.savings_goal, color='red', linewidth=1, linestyle='dotted', label='Savings Goal')

            # Update labels and title
            ax.set_xlabel('Days')
            ax.set_ylabel('Amount ($)')
            ax.set_ylim(bottom=0)
            ax.set_title('Expenses Graph')
            ax.legend(loc='upper right', fontsize = 10)  # Add legend

            # Adjust ticks
            ax.tick_params(axis='both', which='major', labelsize=10)  # Adjust the labelsize as needed

            # Redraw the canvas with the new figure
            self.canvas.draw()

    def get_monthly_balance(self, data):
        categories = ["Food", "Rent", "Utilities", "Transportation", "Shopping", "Life and Entertainment", "Other"]

        # Initialize list to hold monthly expenses
        monthly_balance = []
        balance = data['balance'] + data['income']

        # Iterate over each day
        for day in range(1, 29):  # Use the actual range of days as integers
            day_str = str(day)    # Convert day to string to use as a key in the JSON data
            daily_expenses = []   # List to store daily expenses per category
            

            # Check if the day exists in the data
            for category in categories:
                # Check if the category exists for the day, and sum the expenses if it does
                category_sum = sum(data['expenses'][day_str].get(category, []))
                daily_expenses.append(category_sum)

            # Calculate the total expenses for the day
            daily_total = sum(daily_expenses)
            balance = balance - daily_total

            # Append daily total to monthly expenses
            monthly_balance.append(balance)

        # Print the list of monthly expenses
        return monthly_balance
#############################################################


######################MIAN WINDOW############################
class WINDOW(Tk, Construction):
    def __init__(self, current_user):
        super().__init__()
        self.title('Budget Planner')
        self.configure(bg = '#0b0b0b')
        self.geometry('1512x982')
        self.label = Label(self, text= f"{current_user.capitalize()}'s Budget Planner", font=('Arial', 30), fg = '#b09662', bg = 'black')
        self.label.pack(pady=3)

        # Create a single data manager for the whole application
        self.user_manager = UserDataManager(current_user)
        

        # Pass the data manager to each frame
        FrameRight(self, self.user_manager)
        FrameLeft(self, self.user_manager)
        GraphFrame(self, self.user_manager)
########################################################################


############################MAIN LINE###################################
if __name__ == "__main__":
    #define UserManager class to call in LOGIN class
    user_manager = UserManager()
    login_app = LOGIN(user_manager)


