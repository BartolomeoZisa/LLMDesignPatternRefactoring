import argparse
import os
import sys
import ast
from uml.modules.uml_utils import ClassDependencyVisitor, UMLDiagramDrawer


def main():
    parser = argparse.ArgumentParser(prog='umlgenerator',
                                     description='Generate UML class diagrams from Python code.')
    parser.add_argument('input_path', help='Input Python file or directory to scan')
    parser.add_argument('--output', '-f', default='png',
                        choices=['svg', 'dot', 'png', 'pdf', 'jpg'],
                        help='Output format for UML diagram (default: png)')
    parser.add_argument('--output-directory', '-o', default='uml_output',
                        help='Directory to save UML diagrams (default: uml_output)')
    parser.add_argument('-p', '--project-name', default="classes_diagram",
                        help='Project name prefix for output files')

    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        print(f"Input path does not exist: {args.input_path}", file=sys.stderr)
        sys.exit(1)

    visitor = ClassDependencyVisitor()

    if os.path.isdir(args.input_path):
        dependencies, class_attrs, class_methods = visitor.collect_dependencies_from_directory(args.input_path)
    elif os.path.isfile(args.input_path) and args.input_path.endswith('.py'):
        try:
            with open(args.input_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=args.input_path)
                visitor.visit(tree)
            dependencies, class_attrs, class_methods = visitor.dependencies
        except SyntaxError:
            print(f"Syntax error in file {args.input_path}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Input path must be a Python file or directory: {args.input_path}", file=sys.stderr)
        sys.exit(1)

    project_name = args.project_name or os.path.splitext(os.path.basename(args.input_path))[0]

    drawer = UMLDiagramDrawer(dependencies, class_methods=class_methods,
                                class_attrs=class_attrs,
                             output_dir=args.output_directory,
                             project_name=project_name,
                             output_format=args.output)
    drawer.draw()


if __name__ == '__main__':
    main()




