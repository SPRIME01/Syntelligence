# Documentation Automation

This project implements automated documentation generation using MkDocs, FastAPI, and Pydantic. Documentation is generated from docstrings, type hints, and annotations throughout the codebase, ensuring that API documentation is always up-to-date with the code.

## Documentation Features

- **API Documentation**: Automatically generated from FastAPI routes and Pydantic models
- **Swagger UI & ReDoc**: Interactive API documentation for endpoints
- **MkDocs**: Static documentation site with comprehensive information
- **Docstring Coverage**: Automated checks for documentation completeness
- **CI/CD Integration**: Documentation testing and deployment

## Setup for Development

### Install Documentation Dependencies

```bash
# From the project root
cd backend
pip install -e ".[docs]"
```

### Run Documentation Locally

```bash
# From the project root
mkdocs serve
```

This will start a local server at http://127.0.0.1:8000/ where you can view the documentation.

## Writing Documentation

### Python Docstrings

All Python modules, classes, functions, and methods should include docstrings following Google style format:

```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of the function.

    Longer description explaining what the function does in more detail.

    Args:
        param1: Description of the first parameter
        param2: Description of the second parameter

    Returns:
        Description of the return value

    Raises:
        ValueError: When the function encounters an invalid input
    """
    # Function implementation
```

### FastAPI Route Documentation

FastAPI routes should include comprehensive documentation:

```python
@router.get(
    "/{item_id}",
    response_model=Item,
    summary="Get an item by ID",
    response_description="The requested item"
)
async def get_item(
    item_id: int = Path(..., description="The ID of the item to retrieve", ge=1)
) -> Item:
    """Retrieve a specific item by its ID.

    This endpoint returns details about a specific item identified by its unique ID.

    Args:
        item_id: Unique identifier of the item

    Returns:
        The item object if found

    Raises:
        HTTPException: If item is not found (404) or other error occurs
    """
    # Implementation
```

### Pydantic Models

Document Pydantic models with field descriptions:

```python
class Item(BaseModel):
    """Item model representing a product in the system.

    Attributes:
        id: Unique identifier for the item
        name: The name of the item
        description: Detailed description of the item
        price: The price of the item in USD
        is_available: Whether the item is currently available
    """

    id: int = Field(..., description="Unique identifier for the item")
    name: str = Field(..., description="The name of the item")
    description: str = Field(..., description="Detailed description of the item")
    price: float = Field(..., description="The price of the item in USD", gt=0)
    is_available: bool = Field(True, description="Whether the item is currently available")
```

## Documentation Quality Checks

### Docstring Coverage

A docstring coverage check is included in CI/CD pipelines and available for local use:

```bash
cd backend
python tools/check_docstrings.py --path app --threshold 80 --verbose
```

### Pre-commit Hooks

Pre-commit hooks ensure documentation quality:

```bash
pip install pre-commit
pre-commit install
```

## Documentation Deployment

Documentation is automatically built and deployed via GitHub Actions when changes are pushed to the main branch. The workflow:

1. Builds the documentation site
2. Runs validation checks
3. Deploys to GitHub Pages

## Adding New Documentation Pages

To add new documentation pages:

1. Create a Markdown file in the appropriate folder under `docs/`
2. Add the page to the navigation in `mkdocs.yml`

## API Reference Generation

API reference documentation is automatically generated from the codebase using the `docs/gen_ref_pages.py` script, which:

1. Scans the codebase for Python modules
2. Generates documentation pages using mkdocstrings
3. Builds a navigation structure
