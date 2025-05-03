import json


# Employee class
class Employee:
    def __init__(self, name, age, position, salary):
        self.set_name(name)
        self.set_age(age)
        self.set_position(position)
        self.set_salary(salary)

    def __str__(self):
        return f"{self._name} - {self._position}, Age: {self._age}, Salary: {self._salary}"

    # Setters
    def set_name(self, name):
        self._name = name

    def set_age(self, age):
        if isinstance(age, int) and 18 <= age <= 60:
            self._age = age
        else:
            raise ValueError("Age must be an integer between 18 and 60.")

    def set_position(self, position):
        self._position = position

    def set_salary(self, salary):
        if isinstance(salary, (int, float)) and salary >= 0:
            self._salary = salary
        else:
            raise ValueError(" invalid Salary value.")

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
                elif key == "department":
                    self.set_department(value)
                elif key == "programming_lang":
                    self.set_programming_lang(value)                    

# manager class
class Manager(Employee):
    def __init__(self, name, age, salary, department):
        super().__init__(name, age, "manager", salary)
        self.set_department(department) 

    def __str__(self):
        return super().__str__() + f" Department: {self._department}"

    def set_department(self, department):
        self._department = department

    def get_department(self):
        return self._department


# developer class
class Developer(Employee):
    def __init__(self, name, age, salary, programming_lang):
        super().__init__(name, age, "Developer", salary)
        self.set_programming_lang(programming_lang) 

    def __str__(self):
        return super().__str__() + f" Programming Language: {self._programming_lang}"

    def set_programming_lang(self, programming_lang):
        self._programming_lang = programming_lang

    def get_programming_lang(self):
        return self._programming_lang


# EmployeeManager class
class EmployeeManager:
    def __init__(self):
        self.employees = {}
        self.emp_id = 1

    # input employee data
    def input_employee_data(self, allow_empty=False):
        try:
            input_name = input("Enter name: ")
            input_age = input("Enter age: ")
            input_salary = input("Enter salary: ")
            if allow_empty:
                name = input_name if input_name else None
                age = int(input_age) if input_age else None
                salary = float(input_salary) if input_salary else None
            else:
                if not input_name or not input_age or not input_salary:
                    raise ValueError("All fields are required.")
                name = input_name
                age = int(input_age)
                salary = float(input_salary)
            return name, age, salary
        except ValueError:
            print("Invalid input! Please enter valid numbers for age and salary.")
            return None

    # add employee method
    def add_employee(self):
        print("Add New Employee")
        print("1. General Employee\n2. Manager\n3. Developer")
        try:
            emp_type = int(input("Choose employee type:"))
        except:
            print("Enter valid input")
            return

        data = self.input_employee_data()
        if data is None:
            return
        name, age, salary = data

        if emp_type == 2:
            department = input("Enter department: ")
            emp = Manager(name, age, salary, department)
        elif emp_type == 3:
            prog_lang = input("Enter programming language: ")
            emp = Developer(name, age, salary, prog_lang)
        else:
            position = input("Enter position: ")
            emp = Employee(name, age, position, salary)
        self.employees[self.emp_id] = emp
        print(f"Employee '{emp.get_name()}' added successfully with ID {self.emp_id}")
        self.emp_id += 1
        self.save_to_file()

    # edit employee method
    def edit_employee_data(self):
        try:
            emp_id = int(input("Enter the ID of the employee to edit: "))
            emp = self.employees.get(emp_id)
            if not emp:
                print("Employee not found.")
                return
            data = self.input_employee_data(allow_empty=True)
            if data is None:
                return
            name, age, salary = data
            emp.edit_employee(name=name, age=age, salary=salary)
            if isinstance(emp, Manager):
                department = input("Enter department: ") or None
                emp.edit_employee(department=department)
            elif isinstance(emp, Developer):
                programming_lang = input("Enter programming language: ")
                emp.edit_employee(programming_lang=programming_lang) or None
            self.save_to_file()
            print("Employee data updated successfully.")

        except ValueError:
            print("Invalid input. ID must be an integer.")

    # remove employee method
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

    # search for employee method
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

    # search by id
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

    # updated search by name
    def search_by_name(self):
        emp_name = input("Enter employee Name to search: ").strip().lower()
        found = False
        for emp_id, emp in self.employees.items():
            name = emp.get_name()
            if name and emp_name in name.lower():
                self.print_employee(emp_id, emp)
                found = True
        if not found:
            print("Employee not found.")

    # view all employees
    def view_all_employees(self):
        if not self.employees:
            print("No employees found.")
            return
        for emp_id, emp in self.employees.items():
            self.print_employee(emp_id, emp)

    # show employee data
    def print_employee(self, emp_id, emp):
        print(f"ID: {emp_id} | {emp}")

    # save data to json file
    def save_to_file(self, filename="employee.json"):
        with open(filename, "w") as file:
            data = {}
            for emp_id, emp in self.employees.items():
                emp_data = {
                    "name": emp.get_name(),
                    "age": emp.get_age(),
                    "position": emp.get_position(),
                    "salary": emp.get_salary(),
                }
                if isinstance(emp, Manager):
                    emp_data["department"] = emp.get_department()
                elif isinstance(emp, Developer):
                    emp_data["programming_lang"] = emp.get_programming_lang()
                data[emp_id] = emp_data
            json.dump(data, file, indent=4)
            print("Data saved successfully.")

    # load data
    def load_from_file(self, filename="employee.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for emp_id, emp_info in data.items():
                    # تأكد من تحويل العمر والراتب إلى الأنواع الصحيحة
                    try:
                        age = int(emp_info["age"])
                        salary = float(emp_info["salary"])
                        name = emp_info["name"]
                        position = emp_info.get("position")

                        if emp_info.get("department"):
                            department = emp_info["department"]
                            self.employees[int(emp_id)] = Manager(
                                name=name,
                                age=age,
                                salary=salary,
                                department=department
                            )
                        elif emp_info.get("programming_lang"):
                            prog_lang = emp_info["programming_lang"]
                            self.employees[int(emp_id)] = Developer(
                                name=name,
                                age=age,
                                salary=salary,
                                programming_lang=prog_lang
                            )
                        else:
                            self.employees[int(emp_id)] = Employee(
                                name=name,
                                age=age,
                                position=position,
                                salary=salary
                            )
                    except Exception as e:
                        print(f"Error loading employee with ID {emp_id}: {e}")
            if self.employees:
                self.emp_id = max(self.employees.keys()) + 1
            else:
                self.emp_id = 1
        except FileNotFoundError:
            print("No existing data found, starting fresh.")
        except json.JSONDecodeError:
            print("Data file is corrupted. Starting with empty data.")

    # program menu
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
    general = EmployeeManager()
    general.load_from_file()
    general.user_menu()
