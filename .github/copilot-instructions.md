# GitHub Copilot Custom Instructions

These instructions guide GitHub Copilot to generate code that adheres to best practices and architectural principles. In cases of conflict, these custom instructions take precedence over other guidelines.

---

## Core Principles

- **Readability:** Write clear, concise, and understandable code
- **DRY (Don't Repeat Yourself):** Extract common logic into reusable components
- **KISS (Keep It Simple, Stupid):** Prioritize simplicity in design and implementation
- **YAGNI (You Ain't Gonna Need It):** Avoid unnecessary functionality
- **Composition Over Inheritance:** Build complex objects from smaller components
- **SOLID Principles:** - Single Responsibility (SRP): Each class has one purpose - Open/Closed (OCP): Open for extension, closed for modification - Liskov Substitution (LSP): Subtypes must be substitutable for base types - Interface Segregation (ISP): Clients shouldn't depend on unused interfaces - Dependency Inversion (DIP): Depend on abstractions, not implementations

---

## Code Style & Documentation

- **Naming:** Use descriptive names for all code elements
- **Formatting:** Follow language-specific style guidelines (e.g., PEP8 for Python)
- **Interface-First Design:** Define clear contracts between components
- **Dependency Injection:** Use constructor injection by default
- **Abstractions:** Create interfaces for all major components
- **Documentation:**
  - Document interface contracts clearly
  - Specify dependencies in docstrings
  - Mandatory docstrings for modules, classes, and functions
  - Use Google-style docstrings with Args, Returns, Raises sections
  - Write docstrings that can be extracted by documentation tools (mkdocs, sphinx)
  - Include examples in docstrings for complex functions
  - Document Pydantic fields with clear descriptions for auto-generated API docs
  - Comments explaining the "why" behind code decisions
  - Meaningful type hints without redundancy
  - Ensure consistency in documentation style
- **Encapsulation:**
  - Protect internal state with appropriate access modifiers
  - Use private/protected attributes and methods where applicable
  - Hide implementation details behind interfaces

---

## API Documentation

- Add OpenAPI decorators and metadata to all API endpoints
- Include comprehensive summaries and descriptions for endpoints
- Document response models, status codes, and error responses
- Provide example requests and responses where helpful
- Document authentication and authorization requirements
- Use type annotations that generate clear API schemas
- Organize endpoints with logical tags and grouping
- Ensure Pydantic model field descriptions propagate to API docs

---

## Plugin Architecture

- Define clear plugin interfaces
- Use dependency injection containers
- Implement plugin discovery mechanisms
- Support hot-reloading where applicable
- Maintain backwards compatibility

---

## Function & Method Design

- Keep functions small with a single responsibility
- Minimize side effects and aim for pure functions
- Use meaningful, limited parameters
- Maintain consistent return types
- Apply Command-Query Separation (CQS)

---

## Branch Management

- Never work directly on main/master
- Create feature branches: `git checkout -b feature/<feature-name>` using kebab-case
- Keep features small and focused
- Use pull requests for code reviews
- Commit often with descriptive messages
- Commit Message Format: - 📝 Be extremely detailed with file changes - 🤔 Explain the reasoning behind each change - 🎨 Use relevant emojis to categorize changes - Example: "✨ feat(auth): Add JWT token validation to login endpoint - 🔧 Modified: src/auth/jwt_validator.py - 📦 Added: tests/auth/test_jwt_validator.py - 🔥 Removed: old token validation logic
  Why: Improves security by implementing industry-standard JWT validation"

---

## Language-Specific Standards

### Python

- Follow PEP8 with strict typing (mypy compatible)
- Use typing.protocol for interfaces except where abstract base classes are needed
- Use context managers for resource management
- Employ Pydantic for data structures and validation
  - Add field descriptions to all Pydantic model fields
  - Use validators with descriptive error messages
  - Leverage Pydantic's Config for enhanced documentation
- Implement async methods where beneficial
- Follow Domain-Driven Design principles with ports & adapters pattern
- Configure with `pyproject.toml`
- Virtual environment with `uv`: - Create: `uv venv .venv` - Activate (Windows): `.venv\Scripts\activate` - Activate (Unix): `source .venv/bin/activate`
- Manage dependencies with `uv pip`
- FastAPI specific:
  - Use path operation decorators with complete metadata
  - Document response models and status codes
  - Add examples to complex request/response models
  - Organize routes with proper tagging and Router objects

### TypeScript

- Follow ES6+ with strict type annotations
- Implement modular design with appropriate interfaces
- Handle async errors properly
- Test with Jest or Vitest according to project needs
- Ensure compliance with language-specific best practices

---

## Testing

- **Structure:** Follow AAA (Arrange, Act, Assert) pattern
- **Naming:** Use verbose class names that clearly state the test case
  Example: `test_UserAuthentication_WithValidCredentials_ReturnsToken`
- **Types:** Write unit, integration, and BDD-style tests
- **Practices:** - Ensure test idempotence - Mock external dependencies - Use descriptive test names following the pattern:
  `test_[Feature]_[Scenario]_[ExpectedResult]` - Use descriptive test names - Integrate tests in CI/CD pipelines - Structure each test with clear AAA sections:

  ````python
  def test_Feature_Scenario_ExpectedResult(): # Arrange # Set up test prerequisites

              # Act
              # Execute the action being tested

              # Assert
              # Verify the expected outcomes
          ```
  ````

---

## Production Readiness

- Comprehensive exception handling
- Input validation and security checks
- Resource cleanup
- Testing with appropriate frameworks (pytest for Python, Jest for TypeScript)

---

## Inline Commands & Special Code Blocks

### Commands

- Refactoring: - Python: `# copilot: refactor` - TypeScript: `// copilot: refactor`
- Optimization: - Python: `# copilot: optimize` - TypeScript: `// copilot: optimize`

### Code Blocks

#### Performance Optimization

```python
# BEGIN PERFORMANCE OPTIMIZATION
# END PERFORMANCE OPTIMIZATION
```

```typescript
// BEGIN PERFORMANCE OPTIMIZATION
// END PERFORMANCE OPTIMIZATION
```

#### Security Checks

```python
# BEGIN SECURITY CHECKS
# END SECURITY CHECKS
```

```typescript
// BEGIN SECURITY CHECKS
// END SECURITY CHECKS
```

---

## Architectural Patterns

- Use established patterns (MVC, MVVM, Clean Architecture, Microservices)
- Implement layered architecture for separation of concerns
- For CSS, apply Block Element Modifier (BEM) naming

---

## Example Scenario Guidance

- **Classes:** Prioritize SRP and encapsulation
- **Functions:** Keep focused and free from side effects
- **Tests:** Follow AAA pattern with clear assertions
- **API Calls:** Handle error cases appropriately
- **UI Components:** Ensure accessibility and follow styling guidelines

---

## Documentation Examples

### Python Function Docstring

```python
def process_payment(
    payment_id: str,
    amount: Decimal,
    currency: str = "USD"
) -> PaymentResult:
    """Process a payment transaction.

    This function handles the processing of payment transactions
    through the payment gateway and records the transaction in the
    database.

    Args:
        payment_id: Unique identifier for the payment
        amount: Amount to be processed
        currency: Three-letter currency code (default: USD)

    Returns:
        PaymentResult object containing transaction details and status

    Raises:
        PaymentGatewayError: If the payment gateway is unavailable
        InvalidAmountError: If amount is negative or zero

    Example:
        >>> result = process_payment("pmt_123", Decimal("99.99"))
        >>> result.status
        'completed'
    """
```

### FastAPI Endpoint Documentation

```python
@router.post(
    "/payments",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        500: {"description": "Payment processing error"}
    },
    summary="Create a new payment",
    description="Process a payment and return the transaction details"
)
async def create_payment(
    payment: PaymentCreate = Body(..., description="Payment details to process"),
    current_user: User = Depends(get_current_user)
) -> PaymentResponse:
    """Create and process a new payment.

    This endpoint accepts payment details, validates them, and processes
    the payment through the payment gateway. The payment is associated with
    the authenticated user.

    Args:
        payment: Payment creation request with amount and method
        current_user: Authenticated user from the token

    Returns:
        PaymentResponse with transaction details

    Raises:
        HTTPException:
            - 400 if payment data is invalid
            - 401 if user is not authenticated
            - 403 if user is not authorized
            - 500 if payment processing fails
    """
```

### Pydantic Model Documentation

```python
class PaymentCreate(BaseModel):
    """Payment creation request model.

    This model defines the data required to create a new payment.

    Attributes:
        amount: The payment amount in the specified currency
        currency: Three-letter currency code (default: USD)
        method: Payment method identifier
        description: Optional payment description
    """

    amount: Decimal = Field(
        ...,
        gt=0,
        description="Payment amount (must be greater than zero)",
        example=99.99
    )
    currency: str = Field(
        default="USD",
        min_length=3,
        max_length=3,
        description="Three-letter currency code",
        example="USD"
    )
    method: str = Field(
        ...,
        description="Payment method identifier",
        example="card_visa"
    )
    description: Optional[str] = Field(
        None,
        max_length=255,
        description="Optional payment description",
        example="Subscription payment"
    )

    class Config:
        """Pydantic model configuration."""

        schema_extra = {
            "example": {
                "amount": 99.99,
                "currency": "USD",
                "method": "card_visa",
                "description": "Monthly subscription payment"
            }
        }
```
