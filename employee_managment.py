import json
from abc import ABC, abstractmethod

# Employee class
class Employee(ABC):
    def __init__(self, name, age, role):
        if name is None:
            raise("name is required")
        self._name = name
        self.set_age(age)
        self._role = role

    def __str__(self):
        return f"{self._name} - {self._role}, Age: {self._age}"

    def set_name(self, name):
        self._name = name

    def set_age(self, age):
        if isinstance(age, int) and 18 <= age <= 60:
            self._age = age
        else:
            raise ValueError("Age must be an integer between 18 and 60.")

    def set_role(self, role):
        self._role = role

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def get_role(self):
        return self._role

    def update_emp(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                if key == "name":
                    self.set_name(value)
                elif key == "age":
                    self.set_age(value)
                elif key == "role":
                    self.set_role(value)
                elif hasattr(self, f"set_{key}"):
                    getattr(self, f"set_{key}")(value)

    def work(self):
        print(f"{self._name} is working as {self._role} in general department.")

    @abstractmethod
    def calc_salary(self):
        pass


class Manager(Employee):
    def __init__(self, name, age, department, base_salary, bonus):
        super().__init__(name, age, "manager")
        self._department = department
        self._base_salary = base_salary
        self._bonus = bonus

    def __str__(self):
        return (
            super().__str__()
            + f" Department: {self._department} Salary: {self.calc_salary()}"
        )

    def set_base_salary(self, base_salary):
        self._base_salary = base_salary

    def set_bonus(self, bonus):
        self._bonus = bonus

    def set_department(self, department):
        self._department = department

    def get_department(self):
        return self._department

    def get_base_salary(self):
        return self._base_salary

    def get_bonus(self):
        return self._bonus

    def work(self):
        print(f"{self._name} is managing the {self._department} department.")

    def calc_salary(self):
        return self._base_salary + self._bonus


class Developer(Employee):
    def __init__(self, name, age, programming_lang, hourly_rate, hours_worked):
        super().__init__(name, age, "developer")
        self._programming_lang = programming_lang
        self._hourly_rate = hourly_rate
        self._hours_worked = hours_worked

    def __str__(self):
        return (
            super().__str__()
            + f" Programming Language: {self._programming_lang} Salary: {self.calc_salary()}"
        )

    def set_programming_lang(self, programming_lang):
        self._programming_lang = programming_lang

    def set_hourly_rate(self, hourly_rate):
        self._hourly_rate = hourly_rate

    def set_hours_worked(self, hours_worked):
        self._hours_worked = hours_worked

    def get_programming_lang(self):
        return self._programming_lang

    def get_hourly_rate(self):
        return self._hourly_rate

    def get_hours_worked(self):
        return self._hours_worked

    def work(self):
        print(f"{self._name} is writing code in {self._programming_lang}")

    def calc_salary(self):
        return self._hourly_rate * self._hours_worked


class EmployeeManager:
    def __init__(self):
        self.employees = {}
        self.emp_id = 1001

    def input_employee_data(self, emp_type, allow_empty=False):
        try:
            input_name = input("Enter name: ")
            input_age = input("Enter age: ")

            name = input_name if input_name else None
            age = int(input_age) if input_age else None
            if name is None and not allow_empty:
                raise ValueError("Name is required.")

            if emp_type == 1:
                manager_data = self.input_manager_data()
                if manager_data is None and not allow_empty:
                    raise ValueError("Manager data is required.")
                return name, age, manager_data[0], manager_data[1], manager_data[2], None, None, None
            elif emp_type == 2:
                dev_data = self.input_developer_data()
                if dev_data is None and not allow_empty:
                    raise ValueError("Developer data is required.")
                return name, age, None, None, None, dev_data[0], dev_data[1], dev_data[2]

        except ValueError as e:
            print(e)
            return None

    def input_manager_data(self):
        department = input("Enter department: ") or None
        base_salary_input = input("Enter base salary: ")
        bonus_input = input("Enter bonus: ")
        try:
            base_salary = float(base_salary_input) if base_salary_input else None
            bonus = float(bonus_input) if bonus_input else None
            return department, base_salary, bonus
        except ValueError:
            print("Invalid base salary or bonus input.")
            return None

    def input_developer_data(self):
        prog_lang = input("Enter programming language: ") or None
        hourly_rate_input = input("Enter hourly rate: ")
        work_hours_input = input("Enter work hours: ")
        try:
            hourly_rate = float(hourly_rate_input) if hourly_rate_input else None
            work_hours = float(work_hours_input) if work_hours_input else None
            return prog_lang, hourly_rate, work_hours
        except ValueError:
            print("Invalid hourly rate or work hours input.")
            return None
    def add_employee(self):
        print("Add New Employee")
        print("1. Manager\n2. Developer")
        try:
            emp_type = int(input("Choose employee type: "))
        except ValueError:
            print("Invalid input, must be integer 1 or 2.")
            return

        data = self.input_employee_data(emp_type)
        if data is None:
            return
        name, age, department, base_salary, bonus, prog_lang, hourly_rate, work_hours = data
        try:
            if emp_type == 1:
                emp = Manager(name, age, department, base_salary, bonus)
            elif emp_type == 2:
                emp = Developer(name, age, prog_lang, hourly_rate, work_hours)
            else:
                print("Invalid employee type.")
                return

            self.employees[self.emp_id] = emp
            print(f"Employee '{emp.get_name()}' added successfully with ID {self.emp_id}")
            self.emp_id += 1
            self.save_to_file()
        except ValueError as e:
            print(e)

    def edit_employee_data(self):
        print("Edit Employee")
        try:
            emp_id = int(input("Enter the ID of the employee to edit: "))
        except ValueError:
            print("Invalid input. ID must be an integer.")
            return

        emp = self.employees.get(emp_id)
        if not emp:
            print("Employee not found.")
            return

        emp_type = 1 if isinstance(emp, Manager) else 2
        data = self.input_employee_data(emp_type, allow_empty=True)
        if data is None:
            return

        name, age, department, base_salary, bonus, prog_lang, hourly_rate, work_hours = data
        try:
            if isinstance(emp, Manager):
                emp.update_emp(
                    name=name, age=age, department=department,
                    base_salary=base_salary, bonus=bonus
                )
            elif isinstance(emp, Developer):
                emp.update_emp(
                    name=name, age=age, programming_lang=prog_lang,
                    hourly_rate=hourly_rate, hours_worked=work_hours
                )
            self.save_to_file()
            print("Employee data updated successfully.")
        except ValueError as e:
            print(e)

    def remove_employee(self):
        try:
            emp_id = int(input("Enter the ID to remove: "))
            emp = self.employees.pop(emp_id, None)
            if emp:
                print(f"Employee '{emp.get_name()}' removed successfully.")
                self.save_to_file()
                if not self.employees:
                    self.emp_id = 1001
            else:
                print("Employee not found.")
        except ValueError:
            print("Invalid input. ID must be an integer.")

    def search_employee_menu(self):
        print("1. Search by ID\n2. Search by Name")
        try:
            search_type = int(input("Enter your choice: "))
            if search_type == 1:
                self.search_by_id()
            elif search_type == 2:
                self.search_by_name()
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input, must be an integer.")

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
        emp_name = input("Enter employee name to search: ").strip().lower()
        found = False
        for emp_id, emp in self.employees.items():
            if emp.get_name() and emp_name in emp.get_name().lower():
                self.print_employee(emp_id, emp)
                found = True
        if not found:
            print("Employee not found.")

    def view_all_employees(self):
        if not self.employees:
            print("No employees found.")
            return
        for emp_id, emp in self.employees.items():
            self.print_employee(emp_id, emp)

    def print_employee(self, emp_id, emp):
        print(f"ID: {emp_id} | {emp}")

    def show_work(self):
        try:
            emp_id = int(input("Enter ID of Employee: "))
            emp = self.employees.get(emp_id)
            if not emp:
                print("Employee not found.")
                return
            emp.work()
        except ValueError:
            print("Invalid ID, must be an integer.")

    def save_to_file(self, filename="employee.json"):
        with open(filename, "w") as file:
            data = {}
            for emp_id, emp in self.employees.items():
                emp_data = {
                    "name": emp.get_name(),
                    "age": emp.get_age(),
                    "role": emp.get_role(),
                }
                if isinstance(emp, Manager):
                    emp_data.update({
                        "department": emp.get_department(),
                        "base_salary": emp.get_base_salary(),
                        "bonus": emp.get_bonus()
                    })
                elif isinstance(emp, Developer):
                    emp_data.update({
                        "programming_lang": emp.get_programming_lang(),
                        "hourly_rate": emp.get_hourly_rate(),
                        "hours_worked": emp.get_hours_worked()
                    })
                data[emp_id] = emp_data
            json.dump(data, file, indent=4)
            print("Data saved successfully.")

    def load_from_file(self, filename="employee.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for emp_id_str, emp_info in data.items():
                    emp_id = int(emp_id_str)
                    name = emp_info["name"]
                    age = int(emp_info["age"])
                    if emp_info["role"] == "manager":
                        emp = Manager(name, age, emp_info["department"], emp_info["base_salary"], emp_info["bonus"])
                    elif emp_info["role"] == "developer":
                        emp = Developer(name, age, emp_info["programming_lang"], emp_info["hourly_rate"], emp_info["hours_worked"])
                    else:
                        continue
                    self.employees[emp_id] = emp
                if self.employees:
                    self.emp_id = max(self.employees.keys()) + 1
        except FileNotFoundError:
            print("File not found. Starting with empty employee list.")
        except Exception as e:
            print(f"Error loading data: {e}")
    # program menu
    def user_menu(self):
        menu_options = {
            1: ("Add a new employee", self.add_employee),
            2: ("Edit employee data", self.edit_employee_data),
            3: ("Remove an employee", self.remove_employee),
            4: ("Find an employee", self.search_employee_menu),
            5: ("View all employees", self.view_all_employees),
            6: ("Show Employee Work", self.show_work),
            7: ("Exit", None),
        }

        while True:
            print("\nEmployee Manager Menu:")
            for key, (desc, _) in menu_options.items():
                print(f"{key}. {desc}")

            try:
                user_input = int(input("Enter your choice: "))
                if user_input == 7:
                    print("Exiting program...")
                    self.save_to_file()
                    break
                elif user_input in menu_options:
                    menu_options[user_input][1]()
                else:
                    print("Enter a choice between 1 - 7.")
            except ValueError:
                print("Invalid data type.")


# Main program
if __name__ == "__main__":
    general = EmployeeManager()
    general.load_from_file()
    general.user_menu()