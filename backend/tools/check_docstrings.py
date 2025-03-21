#!/usr/bin/env python
"""Script to check docstring coverage in the codebase.

This script analyzes Python files to ensure they have proper docstrings
for modules, classes, methods, and functions. It can be used as part of
CI/CD pipelines or pre-commit hooks to maintain documentation quality.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Set

import ast
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform colored terminal output
colorama.init()


class DocstringVisitor(ast.NodeVisitor):
    """AST visitor to check for docstrings in code elements."""

    def __init__(self) -> None:
        """Initialize the docstring visitor."""
        self.stats: Dict[str, Dict[str, int]] = {
            "module": {"total": 0, "documented": 0},
            "class": {"total": 0, "documented": 0},
            "function": {"total": 0, "documented": 0},
            "method": {"total": 0, "documented": 0},
        }
        self.undocumented: Dict[str, List[str]] = {
            "module": [],
            "class": [],
            "function": [],
            "method": [],
        }
        self.current_class = None

    def visit_Module(self, node: ast.Module) -> None:
        """Visit a module node and check for module-level docstring.

        Args:
            node: The AST module node
        """
        self.stats["module"]["total"] += 1
        if ast.get_docstring(node):
            self.stats["module"]["documented"] += 1
        else:
            self.undocumented["module"].append("module")
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit a class definition and check for class docstring.

        Args:
            node: The AST class definition node
        """
        self.stats["class"]["total"] += 1
        if ast.get_docstring(node):
            self.stats["class"]["documented"] += 1
        else:
            self.undocumented["class"].append(node.name)

        # Remember the current class for method context
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit a function definition and check for function/method docstring.

        Args:
            node: The AST function definition node
        """
        if self.current_class:
            # This is a method
            self.stats["method"]["total"] += 1
            if ast.get_docstring(node):
                self.stats["method"]["documented"] += 1
            else:
                self.undocumented["method"].append(f"{self.current_class}.{node.name}")
        else:
            # This is a function
            self.stats["function"]["total"] += 1
            if ast.get_docstring(node):
                self.stats["function"]["documented"] += 1
            else:
                self.undocumented["function"].append(node.name)

        self.generic_visit(node)

    def get_coverage(self) -> Dict[str, float]:
        """Calculate the docstring coverage percentages.

        Returns:
            Dictionary with coverage percentages for each code element type
        """
        coverage = {}
        for element_type, counts in self.stats.items():
            if counts["total"] == 0:
                coverage[element_type] = 100.0
            else:
                coverage[element_type] = (counts["documented"] / counts["total"]) * 100.0

        # Calculate overall coverage
        total = sum(counts["total"] for counts in self.stats.values())
        documented = sum(counts["documented"] for counts in self.stats.values())

        if total == 0:
            coverage["overall"] = 100.0
        else:
            coverage["overall"] = (documented / total) * 100.0

        return coverage


def analyze_file(file_path: Path) -> DocstringVisitor:
    """Analyze a Python file for docstring coverage.

    Args:
        file_path: Path to the Python file to analyze

    Returns:
        DocstringVisitor with analysis results

    Raises:
        SyntaxError: If the file contains invalid Python syntax
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        tree = ast.parse(content)
        visitor = DocstringVisitor()
        visitor.visit(tree)
        return visitor
    except SyntaxError as e:
        print(f"{Fore.RED}Syntax error in {file_path}: {e}{Style.RESET_ALL}")
        raise


def find_python_files(directory: Path, exclude_dirs: Set[str]) -> List[Path]:
    """Find all Python files in the given directory recursively.

    Args:
        directory: Root directory to search in
        exclude_dirs: Set of directory names to exclude

    Returns:
        List of paths to Python files
    """
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)

    return python_files


def print_results(visitor: DocstringVisitor, file_path: Path) -> None:
    """Print docstring coverage results for a file.

    Args:
        visitor: DocstringVisitor with analysis results
        file_path: Path to the analyzed file
    """
    coverage = visitor.get_coverage()

    # Determine color based on overall coverage
    if coverage["overall"] >= 90:
        color = Fore.GREEN
    elif coverage["overall"] >= 70:
        color = Fore.YELLOW
    else:
        color = Fore.RED

    print(f"\n{color}Coverage for {file_path}:{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Overall:{Style.RESET_ALL} {color}{coverage['overall']:.1f}%{Style.RESET_ALL}")

    # Print coverage by element type
    for element_type in ["module", "class", "function", "method"]:
        if visitor.stats[element_type]["total"] > 0:
            print(f"  {Fore.CYAN}{element_type.capitalize()}:{Style.RESET_ALL} "
                  f"{color}{coverage[element_type]:.1f}%{Style.RESET_ALL} "
                  f"({visitor.stats[element_type]['documented']}/{visitor.stats[element_type]['total']})")

    # Print undocumented elements
    for element_type, elements in visitor.undocumented.items():
        if elements:
            print(f"\n  {Fore.YELLOW}Undocumented {element_type}s:{Style.RESET_ALL}")
            for element in elements:
                print(f"    - {element}")


def main() -> int:
    """Run the docstring coverage check.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = argparse.ArgumentParser(description="Check docstring coverage in Python files")
    parser.add_argument("--path", type=str, default="backend",
                        help="Path to directory to analyze")
    parser.add_argument("--exclude", type=str, nargs="+", default=["__pycache__", ".venv", "tests"],
                        help="Directories to exclude from analysis")
    parser.add_argument("--threshold", type=float, default=80.0,
                        help="Minimum acceptable docstring coverage percentage")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print detailed information about each file")

    args = parser.parse_args()

    path = Path(args.path)
    exclude_dirs = set(args.exclude)
    threshold = args.threshold
    verbose = args.verbose

    if not path.exists():
        print(f"{Fore.RED}Error: Path {path} does not exist{Style.RESET_ALL}")
        return 1

    python_files = find_python_files(path, exclude_dirs)

    if not python_files:
        print(f"{Fore.YELLOW}No Python files found in {path}{Style.RESET_ALL}")
        return 0

    print(f"{Fore.CYAN}Analyzing {len(python_files)} Python files...{Style.RESET_ALL}")

    total_stats = {
        "module": {"total": 0, "documented": 0},
        "class": {"total": 0, "documented": 0},
        "function": {"total": 0, "documented": 0},
        "method": {"total": 0, "documented": 0},
    }

    for file_path in python_files:
        try:
            visitor = analyze_file(file_path)

            # Update total statistics
            for element_type, counts in visitor.stats.items():
                total_stats[element_type]["total"] += counts["total"]
                total_stats[element_type]["documented"] += counts["documented"]

            if verbose:
                print_results(visitor, file_path)
        except SyntaxError:
            continue

    # Calculate overall coverage
    total_elements = sum(counts["total"] for counts in total_stats.values())
    total_documented = sum(counts["documented"] for counts in total_stats.values())

    if total_elements == 0:
        overall_coverage = 100.0
    else:
        overall_coverage = (total_documented / total_elements) * 100.0

    # Determine color based on overall coverage
    if overall_coverage >= 90:
        color = Fore.GREEN
    elif overall_coverage >= 70:
        color = Fore.YELLOW
    else:
        color = Fore.RED

    print(f"\n{Fore.CYAN}Overall Coverage Summary:{Style.RESET_ALL}")
    print(f"  {color}{overall_coverage:.1f}% ({total_documented}/{total_elements}){Style.RESET_ALL}")

    # Print coverage by element type
    for element_type in ["module", "class", "function", "method"]:
        if total_stats[element_type]["total"] > 0:
            type_coverage = (total_stats[element_type]["documented"] / total_stats[element_type]["total"]) * 100.0
            print(f"  {Fore.CYAN}{element_type.capitalize()}:{Style.RESET_ALL} "
                  f"{color}{type_coverage:.1f}%{Style.RESET_ALL} "
                  f"({total_stats[element_type]['documented']}/{total_stats[element_type]['total']})")

    # Check if coverage meets threshold
    if overall_coverage < threshold:
        print(f"\n{Fore.RED}Error: Docstring coverage ({overall_coverage:.1f}%) "
              f"is below the required threshold ({threshold}%){Style.RESET_ALL}")
        return 1

    print(f"\n{Fore.GREEN}Success: Docstring coverage ({overall_coverage:.1f}%) "
          f"meets or exceeds the required threshold ({threshold}%){Style.RESET_ALL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
