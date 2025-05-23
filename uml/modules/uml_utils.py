import ast
import os
import sys
from graphviz import Digraph


class ClassDependencyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.current_class = None
        self.dependencies = {}
        self.class_attrs = {}
        self.class_methods = {}
        self.known_classes = set()

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.known_classes.add(self.current_class)

        self.dependencies.setdefault(self.current_class, [])
        self.class_attrs.setdefault(self.current_class, set())
        self.class_methods.setdefault(self.current_class, set())

        for base in node.bases:
            if isinstance(base, ast.Name):
                self.dependencies[self.current_class].append(('inherits', base.id))
            elif isinstance(base, ast.Attribute):
                self.dependencies[self.current_class].append(('inherits', base.attr))

        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class:
            args = [arg.arg for arg in node.args.args if arg.arg != 'self']
            method_signature = f"{node.name}({', '.join(args)})"
            self.class_methods[self.current_class].add(method_signature)

            # Check for usage via type hints
            for arg in node.args.args:
                if arg.annotation:
                    self._handle_annotation(arg.annotation, rel_type='uses')

            if node.returns:
                self._handle_annotation(node.returns, rel_type='uses')

        self.generic_visit(node)

    def visit_Assign(self, node):
        if not self.current_class:
            return

        for target in node.targets:
            if (
                isinstance(target, ast.Attribute) and
                isinstance(target.value, ast.Name) and
                target.value.id == 'self'
            ):
                attr_name = target.attr
                self.class_attrs[self.current_class].add(attr_name)

                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    self.dependencies[self.current_class].append(('composes', node.value.func.id))
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        if not self.current_class:
            return

        if (
            isinstance(node.target, ast.Attribute) and
            isinstance(node.target.value, ast.Name) and
            node.target.value.id == 'self'
        ):
            attr_name = node.target.attr
            self.class_attrs[self.current_class].add(attr_name)
            self._handle_annotation(node.annotation, rel_type='composes')

        self.generic_visit(node)

    def visit_Call(self, node):
        if self.current_class and isinstance(node.func, ast.Name):
            self.dependencies[self.current_class].append(('uses', node.func.id))
        self.generic_visit(node)

    def _handle_annotation(self, annotation, rel_type):
        """Extract class names from type annotations."""
        if isinstance(annotation, ast.Name):
            self.dependencies[self.current_class].append((rel_type, annotation.id))
        elif isinstance(annotation, ast.Subscript):  # e.g. List[Foo]
            self._handle_annotation(annotation.value, rel_type)
            if hasattr(annotation.slice, 'value'):
                self._handle_annotation(annotation.slice.value, rel_type)
            elif isinstance(annotation.slice, ast.Name):
                self._handle_annotation(annotation.slice, rel_type)

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
        return self.dependencies, self.class_attrs, self.class_methods



class UMLDiagramDrawer:
    def __init__(self, dependencies, class_attrs, class_methods, output_dir='uml_output', project_name=None, output_format='png'):
        self.dependencies = dependencies
        self.class_attrs = class_attrs
        self.class_methods = class_methods
        self.output_dir = output_dir
        self.project_name = project_name or "uml_class_diagram"
        self.output_format = output_format

    def draw(self):
        os.makedirs(self.output_dir, exist_ok=True)

        dot = Digraph('UML', format=self.output_format)
        dot.attr(rankdir='BT')
        dot.attr(ratio="1")
        dot.attr(nodesep="0.5")
        dot.attr(ranksep="0.5")

        dot.attr('node', shape='record', fontsize='10', fontname='Helvetica', style='filled', fillcolor='white')

        all_classes = set(self.dependencies.keys())

        for cls in sorted(all_classes):
            attrs = "\\l".join(sorted(self.class_attrs.get(cls, []))) + "\\l" if self.class_attrs.get(cls) else ""
            methods = "\\l".join(sorted(self.class_methods.get(cls, []))) + "\\l" if self.class_methods.get(cls) else ""
            label = f"{{ {cls} | {attrs} | {methods} }}"
            dot.node(cls, label=label)

        for cls in sorted(self.dependencies.keys()):
            for rel_type, target in sorted(self.dependencies[cls], key=lambda x: (x[0], x[1])):
                if target not in all_classes or cls == target:
                    continue
                if rel_type == 'inherits':
                    dot.edge(cls, target, arrowhead='empty')
                elif rel_type == 'composes':
                    dot.edge(cls, target, arrowhead='diamond')
                elif rel_type == 'uses':
                    dot.edge(cls, target, arrowhead='vee', style='dashed')

        dot_file_path = os.path.join(self.output_dir, f'{self.project_name}.dot')
        dot.save(dot_file_path)

        output_path = os.path.join(self.output_dir, self.project_name)
        dot.render(output_path, view=False)

        print(f"UML diagram saved:\n- DOT file: {dot_file_path}\n- Rendered image: {output_path}.{self.output_format}")
