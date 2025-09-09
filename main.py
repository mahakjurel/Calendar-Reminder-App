import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime
import json
import os

class CalendarReminderApp:
    def __init__(self, master):
        self.master = master
        master.title("Calendar & Reminder")
        master.geometry("700x550")
        master.configure(bg='#E0F7FA')  # Light blue background

        self.selected_date = tk.StringVar()
        self.reminders = {}
        self.load_reminders()

        # Heading Label
        tk.Label(master, text="📅 Calendar & Reminder", font=("Comic Sans MS", 24, "bold"), bg='#E0F7FA', fg="#004D40").pack(pady=10)

        self.create_widgets()

    def create_widgets(self):
        now = datetime.now()
        self.year = now.year
        self.month = now.month

        # Calendar Frame
        self.calendar_frame = tk.Frame(self.master, bg='#E0F7FA')
        self.calendar_frame.pack(pady=10)

        self.draw_calendar()

        # Reminder Section
        reminder_frame = tk.Frame(self.master, bg='#E0F7FA')
        reminder_frame.pack(pady=10)

        tk.Label(reminder_frame, text="Selected Date:", font=("Arial", 12, "bold"), bg='#E0F7FA').grid(row=0, column=0, sticky="w")
        self.date_label = tk.Label(reminder_frame, text="", font=("Arial", 12), bg='#E0F7FA')
        self.date_label.grid(row=0, column=1, sticky="w")

        self.reminder_entry = tk.Entry(reminder_frame, width=40, font=("Arial", 12))
        self.reminder_entry.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Button(reminder_frame, text="Add Reminder", command=self.add_reminder,
                  font=("Arial", 11), bg="#B2EBF2", relief="flat", bd=0).grid(row=2, column=0, pady=5)
        tk.Button(reminder_frame, text="Show All Reminders", command=self.show_reminders,
                  font=("Arial", 11), bg="#B2EBF2", relief="flat", bd=0).grid(row=2, column=1, pady=5)

        self.reminder_listbox = tk.Listbox(reminder_frame, width=50, height=5, font=("Arial", 11))
        self.reminder_listbox.grid(row=3, column=0, columnspan=2, pady=5)

        tk.Button(reminder_frame, text="Delete Selected Reminder", command=self.delete_reminder,
                  font=("Arial", 11), bg="#FF8A80", fg="white", relief="flat", bd=0).grid(row=4, column=0, columnspan=2)

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        header = tk.Label(self.calendar_frame, text=f"{calendar.month_name[self.month]} {self.year}",
                          font=("Arial", 16, "bold"), bg='#E0F7FA', fg="#00796B")
        header.grid(row=0, column=1, columnspan=5)

        tk.Button(self.calendar_frame, text="<", command=self.prev_month, bg="#B2EBF2", relief="flat").grid(row=0, column=0)
        tk.Button(self.calendar_frame, text=">", command=self.next_month, bg="#B2EBF2", relief="flat").grid(row=0, column=6)

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for idx, day in enumerate(days):
            color = "#D32F2F" if day == "Sun" else "black"
            tk.Label(self.calendar_frame, text=day, font=("Arial", 10, "bold"), bg='#E0F7FA', fg=color).grid(row=1, column=idx)

        month_days = calendar.monthcalendar(self.year, self.month)
        for row_num, week in enumerate(month_days, start=2):
            for col_num, day in enumerate(week):
                if day != 0:
                    btn = tk.Button(self.calendar_frame, text=str(day), width=4, height=2,
                                    font=("Arial", 10), bg="white", relief="groove",
                                    command=lambda d=day: self.select_date(d))
                    if col_num == 6:
                        btn.configure(bg="#FFCDD2")
                    btn.grid(row=row_num, column=col_num, padx=2, pady=2)

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.draw_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.draw_calendar()

    def select_date(self, day):
        date_str = f"{self.year}-{self.month:02d}-{day:02d}"
        self.selected_date.set(date_str)
        self.date_label.config(text=date_str)
        self.show_reminders()

    def add_reminder(self):
        date = self.selected_date.get()
        reminder = self.reminder_entry.get()
        if not date or not reminder:
            messagebox.showwarning("Warning", "Please select a date and enter a reminder.")
            return
        self.reminders.setdefault(date, []).append(reminder)
        self.save_reminders()
        self.reminder_entry.delete(0, tk.END)
        self.show_reminders()

    def show_reminders(self):
        self.reminder_listbox.delete(0, tk.END)
        date = self.selected_date.get()
        for reminder in self.reminders.get(date, []):
            self.reminder_listbox.insert(tk.END, reminder)

    def delete_reminder(self):
        selected_idx = self.reminder_listbox.curselection()
        if not selected_idx:
            return
        date = self.selected_date.get()
        del self.reminders[date][selected_idx[0]]
        if not self.reminders[date]:
            del self.reminders[date]
        self.save_reminders()
        self.show_reminders()

    def save_reminders(self):
        with open("reminders.json", "w") as f:
            json.dump(self.reminders, f)

    def load_reminders(self):
        if os.path.exists("reminders.json"):
            with open("reminders.json", "r") as f:
                self.reminders = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarReminderApp(root)
    root.mainloop()
