import nbformat
import os


def extract_imports_from_notebook(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as file:
        nb = nbformat.read(file, as_version=4)

    imports = set()
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            lines = cell["source"].split("\n")
            for line in lines:
                if line.startswith("import ") or " import " in line:
                    # Handle direct imports like 'import pandas'
                    if line.startswith("import "):
                        lib = line.split()[1].split(".")[0]
                        imports.add(lib)
                    # Handle from imports like 'from sklearn.linear_model import LinearRegression'
                    elif " import " in line:
                        lib = line.split()[1]
                        imports.add(lib)

    return imports
