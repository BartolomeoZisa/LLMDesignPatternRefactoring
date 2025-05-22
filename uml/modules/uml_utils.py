import ast
import os
import sys
from graphviz import Digraph


class ClassDependencyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.current_class = None
        self.dependencies = {}
        self.known_classes = set()

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.known_classes.add(self.current_class)
        self.dependencies.setdefault(self.current_class, [])

        for base in node.bases:
            if isinstance(base, ast.Name):
                self.dependencies[self.current_class].append(('inherits', base.id))

        self.generic_visit(node)
        self.current_class = None

    def visit_Assign(self, node):
        if (
            isinstance(node.targets[0], ast.Attribute) and
            isinstance(node.value, ast.Call) and
            isinstance(node.targets[0].value, ast.Name) and
            node.targets[0].value.id == 'self' and
            isinstance(node.value.func, ast.Name)
        ):
            self.dependencies[self.current_class].append(('composes', node.value.func.id))
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and self.current_class:
            self.dependencies[self.current_class].append(('uses', node.func.id))
        self.generic_visit(node)

    def collect_dependencies_from_directory(self, path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            tree = ast.parse(f.read(), filename=full_path)
                            self.visit(tree)
                    except SyntaxError:
                        print(f"Skipped {full_path} (syntax error)", file=sys.stderr)
        return self.dependencies


class UMLDiagramDrawer:
    def __init__(self, dependencies, output_dir='uml_output', project_name=None, output_format='png'):
        self.dependencies = dependencies
        self.output_dir = output_dir
        self.project_name = project_name or "uml_class_diagram"
        self.output_format = output_format

    def draw(self):
        os.makedirs(self.output_dir, exist_ok=True)

        dot = Digraph('UML', node_attr={'shape': 'record', 'fontsize': '10'})
        classes = set(self.dependencies.keys())
        for cls in classes:
            dot.node(cls, f'{{ {cls} }}')

        for cls, rels in self.dependencies.items():
            for rel_type, target in rels:
                if target not in classes or cls == target:
                    continue
                if rel_type == 'inherits':
                    dot.edge(cls, target, arrowhead='empty')
                elif rel_type == 'composes':
                    dot.edge(cls, target, arrowhead='diamond')
                elif rel_type == 'uses':
                    dot.edge(cls, target, style='dashed', arrowhead='vee')

        dot_file_path = os.path.join(self.output_dir, f'{self.project_name}.dot')
        dot.save(dot_file_path)

        dot.format = self.output_format
        output_path = os.path.join(self.output_dir, self.project_name)
        dot.render(output_path, view=False)

        print(f"UML diagram saved as:\n- {dot_file_path}\n- {output_path}.{self.output_format}")