class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

class CompanyHierarchy:
    def __init__(self, relations):
        self.nodes = {}
        self.root = self.build_graph(relations)
        self.paths = {}
        self.find_paths(self.root, ["Company"])

    def build_graph(self, relations):
        for parent, child in relations:
            if parent not in self.nodes:
                self.nodes[parent] = TreeNode(parent)
            if child not in self.nodes:
                self.nodes[child] = TreeNode(child)
            self.nodes[parent].children.append(self.nodes[child])
        return self.nodes["Company"]

    def find_paths(self, root, path):
        if not root.children:
            self.paths[root.name] = list(path)
        for child in root.children:
            self.find_paths(child, path + [child.name])

    def find_closest_department(self, employees):
        emp_paths = []
        for emp in employees:
            if emp not in self.paths:
                raise ValueError(f"Employee '{emp}' not found in the company.")
            emp_paths.append(self.paths[emp])

        min_length = min(len(p) for p in emp_paths)
        lca = "Company"
        for i in range(min_length):
            current = emp_paths[0][i]
            if all(p[i] == current for p in emp_paths):
                lca = current
            else:
                break
        return lca


# Example usage
relations = [
    ("Company", "DeptA"),
    ("Company", "DeptB"),
    ("DeptA", "Alice"),
    ("DeptA", "Bob"),
    ("DeptB", "Charlie"),
    ("DeptB", "David")
]

company = CompanyHierarchy(relations)

# Example Queries
try:
    print(company.find_closest_department(["Alice", "Bob"]))     # DeptA
    print(company.find_closest_department(["Charlie", "David"])) # DeptB
    print(company.find_closest_department(["Alice", "Charlie"])) # Company
except ValueError as e:
    print(e)
