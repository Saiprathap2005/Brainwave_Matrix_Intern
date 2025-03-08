import tkinter as tk
from tkinter import messagebox, simpledialog
import os

class ATM:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM Interface")
        self.master.geometry("400x500")  
        self.center_window()  
        self.balance = 1000  
        self.pin = self.load_pin() 
        self.is_authenticated = False
        self.Mini_Statement = []  

        self.main_frame = tk.Frame(self.master, bg="black", padx=20, pady=20)
        self.main_frame.pack(expand=True)

        self.create_widgets()

    def center_window(self):

        width = 400
        height = 500

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        self.display_frame = tk.Frame(self.main_frame, bg="black", height=30) 
        self.display_frame.pack(pady=3, fill=tk.X) 

        self.display_label = tk.Label(self.display_frame, text="Welcome to the URS ATM", bg="black", fg="white", font=("Helvetica", 13))
        self.display_label.pack(pady=6)

        self.pin_label = tk.Label(self.main_frame, text="Enter your PIN:", font=("Helvetica", 12), bg="black", fg="white")
        self.pin_label.pack()

        self.pin_entry = tk.Entry(self.main_frame, show='*', font=("Helvetica", 12), bg="#f0f0f0")
        self.pin_entry.pack(pady=5)

        self.login_button = tk.Button(self.main_frame, text="Login", command=self.authenticate, font=("Helvetica", 12), bg="#2196F3", fg="white")
        self.login_button.pack(pady=5)

        self.action_frame = tk.Frame(self.main_frame, bg="black")  
        self.action_frame.pack(pady=20)
        
        button_bg_color = "#FF9800"  
        button_fg_color = "white"  

        self.check_balance_button = tk.Button(self.action_frame, text="Check Balance", command=self.check_balance, width=15, bg=button_bg_color, fg=button_fg_color)
        self.deposit_button = tk.Button(self.action_frame, text="Deposit", command=self.deposit, width=15, bg=button_bg_color, fg=button_fg_color)
        self.withdraw_button = tk.Button(self.action_frame, text="Withdraw", command=self.withdraw, width=15, bg=button_bg_color, fg=button_fg_color)
        self.Mini_Statement_button = tk.Button(self.action_frame, text="Mini Statement", command=self.show_Mini_Statement, width=15, bg=button_bg_color, fg=button_fg_color)
        self.set_pin_button = tk.Button(self.action_frame, text="Set PIN", command=self.set_pin, width=15, bg=button_bg_color, fg=button_fg_color)
        
        self.transaction_button = tk.Button(self.action_frame, text="Transfer", command=self.transfer, width=15, bg=button_bg_color, fg=button_fg_color)

        self.exit_button = tk.Button(self.main_frame, text="Exit", command=self.master.quit, font=("Helvetica", 12), bg="#F44336", fg="white")
        self.exit_button.pack(pady=10)

    def load_pin(self):
        """Load the PIN from a file."""
        if os.path.exists("pin.txt"):
            with open("pin.txt", "r") as file:
                return file.read().strip()
        return "1234"  

    def save_pin(self):
        """Save the current PIN to a file."""
        with open("pin.txt", "w") as file:
            file.write(self.pin)

    def authenticate(self):
        entered_pin = self.pin_entry.get()
        if entered_pin == self.pin:
            self.is_authenticated = True
            self.display_label.config(text="Please Select The Mode You Want.")
            self.pin_entry.config(state='disabled')
            self.login_button.config(state='disabled')

            self.check_balance_button.pack(in_=self.action_frame, pady=5)
            self.deposit_button.pack(in_=self.action_frame, pady=5)
            self.withdraw_button.pack(in_=self.action_frame, pady=5)
            self.Mini_Statement_button.pack(in_=self.action_frame, pady=5)  
            self.set_pin_button.pack(in_=self.action_frame, pady=5)  
            self.transaction_button.pack(in_=self.action_frame, pady=5)  
        else:
            messagebox.showerror("Error", "Incorrect PIN. Please try again.")

    def check_balance(self):
        if self.is_authenticated:
            messagebox.showinfo("Balance", f"Your current balance is: ₹{self.balance:.2f}")
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def deposit(self):
        if self.is_authenticated:
            amount = self.get_amount("Deposit")
            if amount is not None:
                self.balance += amount
                self.Mini_Statement.append({"type": "Deposit", "amount": amount})
                messagebox.showinfo("Success", f"₹{amount:.2f} deposited successfully.\nNew Balance: ₹{self.balance:.2f}")
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def withdraw(self):
        if self.is_authenticated:
            amount = self.get_amount("Withdraw")
            if amount is not None:
                if amount < 100:
                    messagebox.showerror("Error", "Minimum withdrawal amount is ₹100.")
                elif amount <= self.balance:
                    self.balance -= amount
                    self.Mini_Statement.append({"type": "Withdraw", "amount": amount})
                    messagebox.showinfo("Success", f"₹{amount:.2f} withdrawn successfully.\nNew Balance: ₹{self.balance:.2f}")
                else:
                    messagebox.showerror("Error", "Insufficient funds.")
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def show_Mini_Statement(self):
        if self.is_authenticated:
            if self.Mini_Statement:
                history = "\n".join([f"{trans['type']}: ₹{trans['amount']:.2f}" for trans in self.Mini_Statement])
                messagebox.showinfo("Mini_Statement", history)
            else:
                messagebox.showinfo("Mini_Statement", "No transactions made yet.")
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def set_pin(self):
        if self.is_authenticated:
            new_pin = simpledialog.askstring("Set PIN", "Enter new PIN (4 digits):")
            if new_pin and len(new_pin) == 4 and new_pin.isdigit():
                self.pin = new_pin
                self.save_pin()  
                messagebox.showinfo("Success", "PIN changed successfully.")
            else:
                messagebox.showerror("Error", "Invalid PIN. Please enter a 4-digit numeric PIN.")
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def transfer(self):
        if self.is_authenticated:
            recipient_account = simpledialog.askstring("Transfer", "Enter recipient account number:")
            if recipient_account:
                amount = self.get_amount("Transfer")
                if amount is not None:
                    if amount <= self.balance:
                        self.balance -= amount
                        self.Mini_Statement.append({"type": "Transfer to " + recipient_account, "amount": amount})
                        messagebox.showinfo("Success", f"₹{amount:.2f} transferred to account {recipient_account}.\nNew Balance: ₹{self.balance:.2f}")
                    else:
                        messagebox.showerror("Error", "Insufficient funds.")
            else:
                messagebox.showerror("Error", "Recipient account number cannot be empty.")
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def get_amount(self, action):
        amount_str = simpledialog.askstring("Input", f"Enter amount to {action.lower()}:")
        if amount_str is not None:
            try:
                amount = float(amount_str)
                if amount > 0:
                    return amount
                else:
                    messagebox.showerror("Error", "Amount must be positive.")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount entered.")
        return None

if __name__ == "__main__":
    root = tk.Tk()
    atm_app = ATM(root)
    root.mainloop()