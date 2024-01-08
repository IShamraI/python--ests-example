#!/usr/bin/env python
"""
Copyright © 2024 Ivan Shamrai isshamray@gmail.com
"""

import argparse
import ast
import logging
import os
import re
from os.path import basename, splitext

from docstring_parser import parse

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s")
log_format = '%(asctime)s [%(levelname)s] %(message)s'

NODE_TYPES = {
    ast.ClassDef: "Class",
    ast.FunctionDef: "Function",
    ast.Module: "Module",
}


def parse_docstrings(source):
    """Parse Python source code and yield a tuple of ast node instance, name,
    line number and docstring for each function/method, class and module.

    The line number refers to the first line of the docstring. If there is
    no docstring, it gives the first line of the class, funcion or method
    block, and docstring is None.
    """
    return process_node(ast.parse(source))


def process_node(node):
    """Recursive function to obtain ast nodes"""
    node_type = NODE_TYPES.get(type(node))
    docstring_text = ast.get_docstring(node)
    lineno = getattr(node, "lineno", 0)

    if docstring_text:
        docstring = parse(docstring_text)
    else:
        docstring = None

    # Recursion with supported node types
    children = [
        process_node(n) for n in node.body if isinstance(n, tuple(NODE_TYPES))
    ]

    return {
        "type": node_type,
        "name": getattr(node, "name", None),
        "line": lineno,
        "docstring": docstring,
        "docstring_text": docstring_text if docstring_text else "",
        "content": children,
    }


def get_docstrings(source, module_name=None):
    """Parse Python source code from string and print docstrings.

    For each class, method or function and the module, prints a heading with
    the type, name and line number and then the docstring with normalized
    indentation.

    The module name is determined from the filename, or, if the source is
    passed as a string, from the optional `module` argument.

    The line number refers to the first line of the docstring, if present,
    or the first line of the class, funcion or method block, if there is none.
    """
    if hasattr(source, "read"):
        filename = getattr(source, "name")
        source = source.read()

        if not module_name:
            module_name = splitext(basename(filename))[0]

    docstrings = parse_docstrings(source)

    if module_name:
        docstrings["name"] = module_name

    return docstrings


def extract_description_and_steps(docstring):
    description = ""
    steps_with_expected_results = []
    lines = docstring.strip().split('\n')
    current_step = None

    for line in lines:
        if line.strip().endswith("Step:"):
            if current_step is not None:
                steps_with_expected_results.append(current_step)
            current_step = {"step": line.strip()[:-6], "expected_result": ""}
        elif current_step is not None:
            current_step["expected_result"] += line.strip() + ' '

    if current_step is not None:
        steps_with_expected_results.append(current_step)

    return description, steps_with_expected_results


def extract_test_docstrings(test_directory):
    docstrings = []
    for root, _, files in os.walk(test_directory):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as target:
                    docstrings.append(get_docstrings(target))

    return docstrings


def extract_test_case_info(text):
    """NOTE: IT IS ONLY DEMO FUNCTION AND IT SHOULD BE UPDATED"""

    # Regular expressions to match the parts of the test case
    description_pattern = r'^(.*?)(?=Requirement)'
    requirement_pattern = r'Requirement: (.*?)\n'
    step_pattern = r'Step: (.*?)\nExpected: (.*?)\n'

    # Extract the description, requirement, steps, and expected results
    description_match = re.search(description_pattern, text, re.DOTALL | re.MULTILINE)
    requirement_match = re.search(requirement_pattern, text)
    step_matches = re.findall(step_pattern, text, re.DOTALL)

    test_case_description = ""
    if description_match:
        test_case_description = description_match.group(1)

    requirement = ""
    if requirement_match:
        requirement = requirement_match.group(1)

    steps_and_expected = [{"Step": step, "Expected": expected} for step, expected in step_matches]

    return {
        "description": test_case_description,
        "requirement": requirement,
        "steps": steps_and_expected
    }


if __name__ == "__main__":
    # Example to extract docstrings for integration with test management systems
    parser = argparse.ArgumentParser(description="Extract docstrings from test files.")
    parser.add_argument("-p", "--path", nargs="?", default="tests/template/",
                        help="Path to the test folder (default: current directory)")

    parser.add_argument("-l", "--log-level", action="store", type=str.upper, help="Log level", default="INFO",
                        choices=("CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"))
    args = parser.parse_args()

    logging.root.setLevel(args.log_level)
    logging.info(f"Logging is set to: {args.log_level}")

    test_directory = args.path
    logging.info(f"Searching tests in {test_directory}")

    test_docstrings = extract_test_docstrings(test_directory)

    for module_data in test_docstrings:
        if module_data.get("type") != "Module":
            raise RuntimeError("Unexpected data")
        module_name = module_data.get('name')
        module_content = module_data.get('content')
        for module_object in module_content:
            if module_object.get("type") == "Class":
                # logging.info(f"Class: {module_object}")
                class_name = module_object.get('name')
                class_content = module_object.get('content')
                for class_object in class_content:
                    # Filter by test_
                    function_name = class_object.get('name')
                    function_content = class_object.get('content')
                    logging.info(
                        f"{module_name}.py::{class_name}::{function_name} : DocString : {extract_test_case_info(class_object.get('docstring_text'))}")
            elif module_object.get("type") == "Function":
                # Filter by test_
                function_name = module_object.get('name')
                logging.info(f"{module_name}.py::{function_name}::{extract_test_case_info(module_object.get('docstring_text'))}")
            else:
                logging.info(module_object)
                raise RuntimeError("Unexpected type inside class")
