"""Generate the code reference pages and navigation."""

from pathlib import Path
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

# Path to the backend code
src_path = Path("backend/app")
doc_path = Path("api/reference")

# Find Python modules
for path in sorted(src_path.rglob("*.py")):
    module_path = path.relative_to(src_path).with_suffix("")
    doc_file = doc_path / module_path.with_suffix(".md")
    full_doc_path = Path("reference", doc_file)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_file = doc_file.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    # Skip certain modules if needed
    skip_modules = set(["__pycache__"])
    if any(part in skip_modules for part in parts):
        continue

    nav[parts] = doc_file.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(["backend", "app"] + list(parts))
        print(f"# {identifier}", file=fd)
        print("", file=fd)
        print("::: " + identifier, file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

# Generate a navigation summary for the API reference section
with mkdocs_gen_files.open("api/reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
