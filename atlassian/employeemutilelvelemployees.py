class TreeNode:
    def __init__(self, name, is_employee=False):
        self.name = name
        self.children = []
        self.is_employee = is_employee


class CompanyHierarchy:
    def __init__(self, relations, employee_set):
        self.nodes = {}
        self.employee_set = employee_set
        self.root = self.build_graph(relations)
        self.paths = {}
        self.find_paths(self.root, ["Company"])

    def build_graph(self, relations):
        for parent, child in relations:
            if parent not in self.nodes:
                self.nodes[parent] = TreeNode(parent, is_employee=(parent in self.employee_set))
            if child not in self.nodes:
                self.nodes[child] = TreeNode(child, is_employee=(child in self.employee_set))
            self.nodes[parent].children.append(self.nodes[child])
        return self.nodes["Company"]

    def find_paths(self, root, path):
        if root.is_employee:
            self.paths[root.name] = list(path)

        for child in root.children:
            self.find_paths(child, path + [child.name])

    def find_closest_department(self, employees):
        emp_paths = []

        for emp in employees:
            if emp not in self.paths:
                raise ValueError(f"Employee '{emp}' not found in the company.")
            emp_paths.append(self.paths[emp])

        # Find common prefix (LCA)
        min_length = min(len(p) for p in emp_paths)
        lca = "Company"
        for i in range(min_length):
            current = emp_paths[0][i]
            if all(p[i] == current for p in emp_paths):
                lca = current
            else:
                break

        return lca


# Sample company hierarchy (Company → Dept → Employees and subordinates)
relations = [
    ("Company", "DeptA"),
    ("Company", "DeptB"),
    ("DeptA", "Alice"),
    ("DeptA", "Bob"),
    ("Alice", "John"),
    ("Bob", "Sara"),
    ("DeptB", "Charlie"),
    ("DeptB", "David"),
    ("Charlie", "Leo")
]

# List of actual employees (who can have subordinates too)
employee_set = {"Alice", "Bob", "John", "Sara", "Charlie", "David", "Leo"}

# Build the Company Hierarchy
hierarchy = CompanyHierarchy(relations, employee_set)

# Example Queries
try:
    print(hierarchy.find_closest_department(["John", "Sara"]))       # DeptA
    print(hierarchy.find_closest_department(["Leo", "David"]))       # DeptB
    print(hierarchy.find_closest_department(["John", "Leo"]))        # Company
    print(hierarchy.find_closest_department(["Alice", "Bob"]))       # DeptA
    print(hierarchy.find_closest_department(["Charlie", "Leo"]))     # DeptB
except ValueError as e:
    print(e)
