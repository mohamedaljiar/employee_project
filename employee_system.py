import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class Employee(ABC):
    def __init__(self, name: str, emp_id: str, base_salary: float):
        self.name = name
        self.__emp_id = emp_id
        self.__base_salary = max(0.0, float(base_salary))

    def get_emp_id(self) -> str:
        return self.__emp_id

    def get_base_salary(self) -> float:
        return self.__base_salary

    def set_base_salary(self, amount: float) -> None:
        if amount >= 0:
            self.__base_salary = float(amount)
        else:
            raise ValueError("Salary must be a positive value.")

    @abstractmethod
    def calculate_pay(self) -> float:
        pass

    @abstractmethod
    def get_details(self) -> str:
        pass


class FullTimeEmployee(Employee):
    def __init__(self, name: str, emp_id: str, base_salary: float, bonus: float = 0.0):
        super().__init__(name, emp_id, base_salary)
        self.bonus = max(0.0, float(bonus))

    def calculate_pay(self) -> float:
        return self.get_base_salary() + self.bonus

    def get_details(self) -> str:
        return f"[Full-Time] ID: {self.get_emp_id()} | Name: {self.name} | Pay: ${self.calculate_pay():,.2f} (Bonus: ${self.bonus:,.2f})"


class ContractEmployee(Employee):
    def __init__(self, name: str, emp_id: str, hourly_rate: float, hours_worked: float):
        super().__init__(name, emp_id, hourly_rate)
        self.hours_worked = max(0.0, float(hours_worked))

    def calculate_pay(self) -> float:
        return self.get_base_salary() * self.hours_worked

    def get_details(self) -> str:
        return f"[Contract] ID: {self.get_emp_id()} | Name: {self.name} | Pay: ${self.calculate_pay():,.2f} ({self.hours_worked} hrs @ ${self.get_base_salary():,.2f}/hr)"


class CompanySystem:
    def __init__(self):
        self.__employees: dict[str, Employee] = {}

    def add_employee(self, emp: Employee) -> Tuple[bool, str]:
        if emp.get_emp_id() in self.__employees:
            return False, "Employee ID already exists."
        self.__employees[emp.get_emp_id()] = emp
        return True, "Employee added successfully."

    def get_all_employees(self) -> List[Employee]:
        return list(self.__employees.values())

    def search_employees(self, query: str) -> List[Employee]:
        query = query.lower()
        return [
            emp for emp in self.__employees.values()
            if query in str(emp.get_emp_id()).lower() or query in emp.name.lower()
        ]

    def delete_employee(self, emp_id: str) -> Tuple[bool, str]:
        if emp_id in self.__employees:
            del self.__employees[emp_id]
            return True, "Employee deleted successfully."
        return False, "Employee not found."

    def update_employee(self, emp_id: str, name: str, val1: float, val2: float, is_fulltime: bool = True) -> Tuple[bool, str]:
        if emp_id not in self.__employees:
            return False, "Employee not found."

        if is_fulltime:
            updated_emp = FullTimeEmployee(name, emp_id, val1, val2)
        else:
            updated_emp = ContractEmployee(name, emp_id, val1, val2)

        self.__employees[emp_id] = updated_emp
        return True, "Employee updated successfully."


class CompanyApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Company Employee Management System")
        self.root.geometry("850x640")

        self.company = CompanySystem()

        self._build_ui()
        self.refresh_table()

    def _build_ui(self) -> None:
        header = ttk.Label(self.root, text="Employee Management System", font=("Segoe UI", 16, "bold"))
        header.pack(pady=12)

        form_frame = ttk.LabelFrame(self.root, text="Employee Registration Form", padding=12)
        form_frame.pack(fill="x", padx=15, pady=5)

        ttk.Label(form_frame, text="Employee ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_id = ttk.Entry(form_frame, width=22)
        self.ent_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Full Name:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_name = ttk.Entry(form_frame, width=22)
        self.ent_name.grid(row=0, column=3, padx=5, pady=5)

        self.lbl_val1 = ttk.Label(form_frame, text="Base Salary ($):")
        self.lbl_val1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_val1 = ttk.Entry(form_frame, width=22)
        self.ent_val1.grid(row=1, column=1, padx=5, pady=5)

        self.lbl_val2 = ttk.Label(form_frame, text="Bonus ($):")
        self.lbl_val2.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_val2 = ttk.Entry(form_frame, width=22)
        self.ent_val2.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Type:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.type_var = tk.StringVar(value="Full-Time")
        rb_ft = ttk.Radiobutton(form_frame, text="Full-Time", variable=self.type_var, value="Full-Time", command=self._update_labels)
        rb_ct = ttk.Radiobutton(form_frame, text="Contract", variable=self.type_var, value="Contract", command=self._update_labels)
        rb_ft.grid(row=2, column=1, sticky="w")
        rb_ct.grid(row=2, column=1, padx=90, sticky="w")

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=12)

        ttk.Button(btn_frame, text="Add Employee", command=self.add_record, width=13).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_record, width=13).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_record, width=13).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_entries, width=13).pack(side="left", padx=5)

        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill="x", padx=15, pady=5)

        ttk.Label(search_frame, text="Search (ID/Name):").pack(side="left", padx=5)
        self.ent_search = ttk.Entry(search_frame)
        self.ent_search.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_record, width=10).pack(side="left", padx=2)
        ttk.Button(search_frame, text="Reset", command=self.refresh_table, width=10).pack(side="left", padx=2)

        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("ID", "Type", "Name", "Total Pay", "Details")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != "Details" else 360)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

    def _update_labels(self) -> None:
        if self.type_var.get() == "Full-Time":
            self.lbl_val1.config(text="Base Salary ($):")
            self.lbl_val2.config(text="Bonus ($):")
        else:
            self.lbl_val1.config(text="Hourly Rate ($):")
            self.lbl_val2.config(text="Hours Worked:")

    def refresh_table(self, items_list: Optional[List[Employee]] = None) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        employees = items_list if items_list is not None else self.company.get_all_employees()
        for emp in employees:
            emp_type = "Full-Time" if isinstance(emp, FullTimeEmployee) else "Contract"
            self.tree.insert("", "end", values=(
                emp.get_emp_id(),
                emp_type,
                emp.name,
                f"${emp.calculate_pay():,.2f}",
                emp.get_details()
            ))

    def add_record(self) -> None:
        emp_id = self.ent_id.get().strip()
        name = self.ent_name.get().strip()
        val1 = self.ent_val1.get().strip()
        val2 = self.ent_val2.get().strip() or "0"

        if not emp_id or not name or not val1:
            messagebox.showwarning("Validation Error", "ID, Name, and Salary/Rate are required.")
            return

        try:
            v1, v2 = float(val1), float(val2)
        except ValueError:
            messagebox.showerror("Validation Error", "Salary/Rate and Bonus/Hours must be numbers.")
            return

        if self.type_var.get() == "Full-Time":
            emp = FullTimeEmployee(name, emp_id, v1, v2)
        else:
            emp = ContractEmployee(name, emp_id, v1, v2)

        success, msg = self.company.add_employee(emp)
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", msg)

    def search_record(self) -> None:
        query = self.ent_search.get().strip()
        if not query:
            self.refresh_table()
            return
        results = self.company.search_employees(query)
        self.refresh_table(results)

    def delete_record(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select an employee from the table.")
            return

        item_values = self.tree.item(selected[0], "values")
        emp_id = item_values[0]

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Employee ID: {emp_id}?"):
            success, msg = self.company.delete_employee(emp_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_table()
                self.clear_entries()

    def update_record(self) -> None:
        emp_id = self.ent_id.get().strip()
        if not emp_id:
            messagebox.showwarning("Validation Error", "Please select an employee or enter an ID.")
            return

        name = self.ent_name.get().strip()
        val1 = self.ent_val1.get().strip()
        val2 = self.ent_val2.get().strip() or "0"
        is_ft = (self.type_var.get() == "Full-Time")

        try:
            v1, v2 = float(val1), float(val2)
        except ValueError:
            messagebox.showerror("Validation Error", "Salary/Rate and Bonus/Hours must be numbers.")
            return

        success, msg = self.company.update_employee(emp_id, name, v1, v2, is_ft)
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", msg)

    def on_item_select(self, event: tk.Event) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        item_values = self.tree.item(selected[0], "values")
        emp_id = item_values[0]

        employees = self.company.get_all_employees()
        emp = next((e for e in employees if e.get_emp_id() == emp_id), None)
        if not emp:
            return

        self.ent_id.config(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_id.insert(0, emp.get_emp_id())
        self.ent_id.config(state="disabled")

        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, emp.name)

        if isinstance(emp, FullTimeEmployee):
            self.type_var.set("Full-Time")
            self._update_labels()
            self.ent_val1.delete(0, tk.END)
            self.ent_val1.insert(0, str(emp.get_base_salary()))
            self.ent_val2.delete(0, tk.END)
            self.ent_val2.insert(0, str(emp.bonus))
        elif isinstance(emp, ContractEmployee):
            self.type_var.set("Contract")
            self._update_labels()
            self.ent_val1.delete(0, tk.END)
            self.ent_val1.insert(0, str(emp.get_base_salary()))
            self.ent_val2.delete(0, tk.END)
            self.ent_val2.insert(0, str(emp.hours_worked))

    def clear_entries(self):
        self.ent_id.config(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_val1.delete(0, tk.END)
        self.ent_val2.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CompanyApp(root)
    root.mainloop()