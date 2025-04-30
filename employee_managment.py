import json
import os

# Employee class
class Employee:
    def __init__(self, name, age, position, salary):
        self._name = name
        self._age = age
        self._position = position
        self._salary = salary
        
    def __str__(self):
        return f"{self._name} - {self._position}, Age: {self._age}, Salary: {self._salary}"
    # Setters
    def set_name(self, name):
        self._name = name

    def set_age(self, age):
        if isinstance(age, int) and 18 <= age <= 60:
            self._age = age
        else:
            print("Age must be an integer between 18 and 60.")

    def set_position(self, position):
        self._position = position

    def set_salary(self, salary):
        if isinstance(salary, (int, float)) and salary >= 0:
            self._salary = salary
        else:
            print("Salary can't be negative.")

    # Getters
    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def get_position(self):
        return self._position

    def get_salary(self):
        return self._salary

    def edit_employee(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                if key == "name":
                    self.set_name(value)
                elif key == "age":
                    self.set_age(value)
                elif key == "position":
                    self.set_position(value)
                elif key == "salary":
                    self.set_salary(value)

# EmployeeManager class
class EmployeeManager:
    def __init__(self):
        self.employees = {}
        self.emp_id = 1

    def input_employee_data(self):
        try:
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            position = input("Enter position: ")
            salary = float(input("Enter salary: "))
            return name, age, position, salary
        except ValueError:
            print("Invalid input! Please enter valid numbers for age and salary.")
            return None

    def add_employee(self):
        print("Add New Employee")
        data = self.input_employee_data()
        if data is None:
            return
        name, age, position, salary = data
        emp = Employee(name, age, position, salary)
        self.employees[self.emp_id] = emp
        print(f"Employee '{emp.get_name()}' added successfully with ID {self.emp_id}")
        self.emp_id += 1
        self.save_to_file()

    def edit_employee_data(self):
        try:
            emp_id = int(input("Enter the ID of the employee to edit: "))
            emp = self.employees.get(emp_id)
            if not emp:
                print("Employee not found.")
                return
            data = self.input_employee_data()
            if data is None:
                return
            name, age, position, salary = data
            emp.edit_employee(name=name, age=age, position=position, salary=salary)
            print("Employee data updated successfully.")
            self.save_to_file()
        except ValueError:
            print("Invalid input. ID must be an integer.")

    def remove_employee(self):
        try:
            emp_id = int(input("Enter the ID to remove: "))
            emp = self.employees.pop(emp_id, None)
            if emp:
                print(f"Employee '{emp.get_name()}' removed successfully.")
                self.save_to_file()
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
            print("Invalid input! Please enter a valid integer.")

    def search_by_name(self):
        emp_name = input("Enter employee Name to search: ").strip().lower()
        found = False
        for emp_id, emp in self.employees.items():
            if emp_name in emp.get_name().lower():
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
            if search_type in search_menu:
                search_menu[search_type][1]()
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input, must be an integer.")

    def view_all_employees(self):
        if not self.employees:
            print("No employees found.")
            return
        for emp_id, emp in self.employees.items():
            self.print_employee(emp_id, emp)

    def print_employee(self, emp_id, emp):
        print(f"ID: {emp_id} | {emp}")

    def save_to_file(self, filename="employee.json"):

        with open(filename, "w") as file:
            data = {}
            for emp_id, emp in self.employees.items():
                data[str(emp_id)] = {
                    "name": emp.get_name(),
                    "age": emp.get_age(),
                    "position": emp.get_position(),
                    "salary": emp.get_salary()
                }
            json.dump(data, file, indent=4)
            print("Data saved successfully.")

    def load_from_file(self, filename="employee.json"):
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
            2: ("Edit employee data", self.edit_employee_data),
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

# Main program
if __name__ == "__main__":
    manager = EmployeeManager()
    manager.load_from_file()
    manager.user_menu()
