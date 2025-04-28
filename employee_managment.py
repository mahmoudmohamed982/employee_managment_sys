import json
import tkinter as tk
window=tk.Tk()
window.title("Employee manager")
window.geometry("400x300")
window.mainloop()
class Employee:
    def __init__(self, name, age, position, salary):
        self.name = name
        self.age = age
        self.position = position
        self.salary = salary

    def edit_employee(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)


class EmployeeManager:
    def __init__(self):
        self.employees = {}
        self.emp_id = 1

    def input_employee_data(self):
        try:
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            salary = float(input("Enter salary: "))
            position = input("Enter position: ")
            return Employee(name, age, position, salary)
        except ValueError:
            print("Invalid input! Please enter valid numbers for age and salary.")
            return None

    def add_employee(self):
        print("Add New Employee")
        emp = self.input_employee_data()
        if emp:
            self.employees[self.emp_id] = emp
            print(f"Employee '{emp.name}' added successfully with ID {self.emp_id}")
            self.emp_id += 1
            self.save_to_file()  # moved inside to ensure only on success

    def remove_employee(self):
        try:
            emp_id = int(input("Enter the ID to remove: "))
            emp = self.employees.pop(emp_id, None)
            if emp:
                print(f"Employee '{emp.name}' removed successfully.")
                self.save_to_file()
                # If no employees left, reset emp_id to 1
                if not self.employees:
                    self.emp_id = 1
            else:
                print("Employee not found.")
        except ValueError:
            print("Invalid input. ID must be an integer.")

    def search_by_id(self):
        try:
            emp_id = int(input("Enter employee ID to search: "))
            emp = self.employees.get(emp_id)
            if emp:
                self.print_employee(emp_id, emp)
            else:
                print("Employee not found.")
        except ValueError:
            print("Invalid input! Please enter a valid integer")

    def search_by_name(self):
        emp_name = input("Enter employee Name to search: ").strip().lower()
        found = False
        for emp_id, emp in self.employees.items():
            if emp_name in emp.name.lower():
                self.print_employee(emp_id, emp)
                found = True
        if not found:
            print("Employee not found.")

    def search_employee_menu(self):
        search_menu = {
            1: ("Search by ID", self.search_by_id),
            2: ("Search by Name", self.search_by_name)
        }
        for key, (value, _) in search_menu.items():
            print(f"{key}. {value}")
        try:
            search_type = int(input("Enter your choice: "))
            if search_type == 1:
                self.search_by_id()
            elif search_type == 2:
                self.search_by_name()
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input, must be an integer.")

    def view_all_employees(self):
        if not self.employees:
            print("No employees found.")
            return
        for emp_id, emp in self.employees.items():
            self.print_employee(emp_id, emp)

    def print_employee(self, emp_id, emp):
        print(f"ID: {emp_id} | Name: {emp.name} | Age: {emp.age} | Position: {emp.position} | Salary: {emp.salary}")

    def edit_employee(self):
        try:
            emp_id = int(input("Enter the ID of the employee to edit: "))
            emp = self.employees.get(emp_id)
            if not emp:
                print("Employee not found.")
                return
            new_name = input("New name: ") or None
            try:
                new_age_input = input("New age: ")
                new_age = int(new_age_input) if new_age_input else None
                new_salary_input = input("New salary: ")
                new_salary = float(new_salary_input) if new_salary_input else None
            except ValueError:
                print("Invalid number entered.")
                return
            new_position = input("New position: ") or None
            emp.edit_employee(name=new_name, age=new_age, position=new_position, salary=new_salary)
            print("Employee data updated successfully.")
            self.save_to_file()
        except ValueError:
            print("Invalid input. ID must be an integer.")

    def save_to_file(self, filename="employee manager/employee.json"):
        with open(filename, "w") as file:
            data = {}
            for emp_id, emp in self.employees.items():
                data[str(emp_id)] = {
                    "name": emp.name,
                    "age": emp.age,
                    "salary": emp.salary,
                    "position": emp.position
                }
            json.dump(data, file, indent=4)
        print("Data saved successfully.")

    def load_from_file(self, filename="employee manager/employee.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for emp_id, emp_info in data.items():
                    self.employees[int(emp_id)] = Employee(
                        name=emp_info["name"],
                        age=emp_info["age"],
                        position=emp_info["position"],
                        salary=emp_info["salary"]
                    )
            if self.employees:
                self.emp_id = max(self.employees.keys()) + 1
            else:
                self.emp_id = 1
        except FileNotFoundError:
            print("No existing data found, starting fresh.")
        except json.JSONDecodeError:
            print("Data file is corrupted. Starting with empty data.")

    def user_menu(self):
        menu_options = {
            1: ("Add a new employee", self.add_employee),
            2: ("Edit employee data", self.edit_employee),
            3: ("Remove an employee", self.remove_employee),
            4: ("Find an employee", self.search_employee_menu),
            5: ("View all employees", self.view_all_employees),
            6: ("Exit", None),
        }

        while True:
            print("\nEmployee Manager Menu:")
            for key, (desc, _) in menu_options.items():
                print(f"{key}. {desc}")

            try:
                user_input = int(input("Enter your choice: "))
                if user_input == 6:
                    print("Exiting program...")
                    self.save_to_file()
                    break
                elif user_input in menu_options:
                    menu_options[user_input][1]()
                else:
                    print("Enter a choice between 1 - 6.")
            except ValueError:
                print("Invalid data type.")

if __name__ == "__main__":
    manager = EmployeeManager()
    manager.load_from_file()
    manager.user_menu()
