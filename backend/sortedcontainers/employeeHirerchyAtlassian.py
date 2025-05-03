from collections import defaultdict

class EmployeeHirerchy:
    def __init__(self, relations):
        self.relations = relations
        self.graph = defaultdict(set)
        self.paths = {}
        self.buildGraph()

    def buildGraph(self):
        for parent, child in relations:
            if parent not in self.graph:
                self.graph[parent] = set()
            if child not in self.graph:
                self.graph[child] = set()
            self.graph[parent].add(child)
        return self.graph
    
    def buildPath(self, parent, path):
        childs = self.graph[parent]

        if not childs:
            self.paths[parent] = path

        for c in childs:
            self.buildPath(c, path + [c])

    def find_closest_department(self, emps):
        
        return 
        



relations = [
    ("Company", "DeptA"),
    ("Company", "DeptB"),
    ("DeptA", "Alice"),
    ("DeptA", "Bob"),
    ("DeptB", "Charlie"),
    ("DeptB", "David")
]

company = EmployeeHirerchy(relations)

print(company.buildGraph())
print(company.find_closest_department(["Alice", "Bob"]))     # DeptA
