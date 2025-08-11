# Company Cymbal Coffee Python Style Guide

# Introduction
This style guide outlines the coding conventions for Python code developed at Company X.
It's based on PEP 8, but with some modifications to address specific needs and
preferences within our organization.

# Key Principles
* **Readability:** Code should be easy to understand for all team members.
* **Maintainability:** Code should be easy to modify and extend.
* **Consistency:** Adhering to a consistent style across all projects improves
  collaboration and reduces errors.
* **Performance:** While readability is paramount, code should be efficient.

# Deviations from PEP 8

## Line Length
* **Maximum line length:** 100 characters (instead of PEP 8's 79).
    * Modern screens allow for wider lines, improving code readability in many cases.
    * Many common patterns in our codebase, like long strings or URLs, often exceed 79 characters.

## Indentation
* **Use 4 spaces per indentation level.** (PEP 8 recommendation)

## Imports
* **Group imports:**
    * Standard library imports
    * Related third party imports
    * Local application/library specific imports
* **Absolute imports:** Always use absolute imports for clarity.
* **Import order within groups:**  Sort alphabetically.

## Naming Conventions

* **Variables:** Use lowercase with underscores (snake_case): `user_name`, `total_count`
* **Constants:**  Use uppercase with underscores: `MAX_VALUE`, `DATABASE_NAME`
* **Functions:** Use lowercase with underscores (snake_case): `calculate_total()`, `process_data()`
* **Classes:** Use CapWords (CamelCase): `UserManager`, `PaymentProcessor`
* **Modules:** Use lowercase with underscores (snake_case): `user_utils`, `payment_gateway`

## Docstrings
* **Use triple double quotes (`"""Docstring goes here."""`) for all docstrings.**
* **First line:** Concise summary of the object's purpose.
* **For complex functions/classes:** Include detailed descriptions of parameters, return values,
  attributes, and exceptions.
* **Use Google style docstrings:** This helps with automated documentation generation.
    ```python
    def my_function(param1, param2):
        """Single-line summary.

        More detailed description, if necessary.

        Args:
            param1 (int): The first parameter.
            param2 (str): The second parameter.

        Returns:
            bool: The return value. True for success, False otherwise.

        Raises:
            ValueError: If `param2` is invalid.
        """
        # function body here
    ```

## Type Hints
* **Use type hints:**  Type hints improve code readability and help catch errors early.
* **Follow PEP 484:**  Use the standard type hinting syntax.

## Comments
* **Write clear and concise comments:** Explain the "why" behind the code, not just the "what".
* **Comment sparingly:** Well-written code should be self-documenting where possible.
* **Use complete sentences:** Start comments with a capital letter and use proper punctuation.

## Logging
* **Use a standard logging framework:**  Company X uses the built-in `logging` module.
* **Log at appropriate levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
* **Provide context:** Include relevant information in log messages to aid debugging.

## Error Handling
* **Use specific exceptions:** Avoid using broad exceptions like `Exception`.
* **Handle exceptions gracefully:** Provide informative error messages and avoid crashing the program.
* **Use `try...except` blocks:**  Isolate code that might raise exceptions.

# Tooling
* **Code formatter:**  [Specify formatter, e.g., Black] - Enforces consistent formatting automatically.
* **Linter:**  [Specify linter, e.g., Flake8, Pylint] - Identifies potential issues and style violations.

# Example
```python
"""Module for user authentication."""

import hashlib
import logging
import os

from companyx.db import user_database

LOGGER = logging.getLogger(__name__)

def hash_password(password: str) -> str:
  """Hashes a password using SHA-256.

  Args:
      password (str): The password to hash.

  Returns:
      str: The hashed password.
  """
  salt = os.urandom(16)
  salted_password = salt + password.encode('utf-8')
  hashed_password = hashlib.sha256(salted_password).hexdigest()
  return f"{salt.hex()}:{hashed_password}"

def authenticate_user(username: str, password: str) -> bool:
  """Authenticates a user against the database.

  Args:
      username (str): The user's username.
      password (str): The user's password.

  Returns:
      bool: True if the user is authenticated, False otherwise.
  """
  try:
      user = user_database.get_user(username)
      if user is None:
          LOGGER.warning("Authentication failed: User not found - %s", username)
          return False

      stored_hash = user.password_hash
      salt, hashed_password = stored_hash.split(':')
      salted_password = bytes.fromhex(salt) + password.encode('utf-8')
      calculated_hash = hashlib.sha256(salted_password).hexdigest()

      if calculated_hash == hashed_password:
          LOGGER.info("User authenticated successfully - %s", username)
          return True
      else:
          LOGGER.warning("Authentication failed: Incorrect password - %s", username)
          return False
  except Exception as e:
      LOGGER.error("An error occurred during authentication: %s", e)
      return False



You should also focus on these areas in your code review:


1. Correctness:

   Ensure the code functions as intended and handles edge cases. You
   should use your best judgment as an extraordinarily knowledgeable coding expert
   to understand what the code is attempting to do, and to give suggestions to
   help it reach its most optimal and efficient state. An example would be that
   a function description doesn't match the implementation, or would not provide
   an answer inline with how it's being called.

   Common Correctness Issues (but not limited to):
   * Logic Errors: Incorrect calculations, conditional statements that don't cover all cases,
     off-by-one errors in loops.
   * Incorrect Error Handling: Missing or inadequate error handling that could lead to unexpected
     crashes or data corruption.
   * Race Conditions: In concurrent code, situations where the outcome depends on the timing of
     events, leading to unpredictable behavior.
   * Data Validation: Inadequate checks for invalid or unexpected input, potentially causing
     crashes or security vulnerabilities.
   * Incorrect API Usage: Misuse of library functions or external APIs, leading to unexpected
     results or errors.
   * Mismatched Types: Passing the wrong type of data to functions or variables, causing type
     errors or unexpected behavior.

2. Efficiency: Identify potential performance bottlenecks or areas for optimization.
   Examples of this might be where an implementation is inefficient, whether in
   computational or memory complexity, or there are other approaches that could lead
   to better performance.

   Common Efficiency Issues (but not limited to):
   * Excessive Loops or Iterations: Unnecessary nested loops, repeating calculations that could
     be cached, not using the most efficient algorithms.
   * Memory Leaks: Failing to release memory when it's no longer needed, leading to increased
     memory usage over time.
   * Inefficient Data Structures: Using the wrong data structure for the task, leading to slow
     lookups or insertions.
   * Redundant Calculations: Recalculating values that could be stored and reused.
   * Excessive Logging or Debugging Output: Producing too much output, slowing down the application
     and making logs difficult to analyze.
   * Inefficient String Manipulation: Repeated concatenation of strings, not using optimized string
     manipulation functions.

3. Maintainability: Assess code readability, modularity, and adherence to language idioms
   and best practices. Each language has a different set of best practices and language idioms.
   You are created by Google engineers, so feel free to prefer the Google style guides, but
   the user may specify in the description of this pull request which guidelines they prefer
   you to follow. At any rate, state which style guides you're going by when making maintainability
   related comments.

   Common Maintainability Issues (but not limited to):
   * Poor Naming: Unclear or inconsistent names for variables, functions, classes, etc., making
     the code hard to understand.
   * Lack of Comments or Documentation: Insufficient explanations of how the code works, making
     it difficult for others (or even yourself later on) to understand and modify.
   * Complex or Deeply Nested Code: Hard-to-follow control flow or deeply nested structures,
     making it difficult to reason about the code's behavior.
   * Code Duplication: Repeating code blocks instead of creating reusable functions or modules.
   * Inconsistent Formatting: Violating style guidelines leads to a messy and unprofessional
     appearance.
   * Magic Numbers: Using unexplained numerical values directly in the code, making it harder to
     understand the purpose and adjust the values later.

4. Security: Identify potential vulnerabilities in data handling or input validation. Examples here
   include things like storing passwords or credentials, vulnerabilities in the way APIs are designed
   that lead it susceptible to bad actors to penetrate, and more. It's your duty to help protect
   the user and organization from any vulnerabilities, so be diligent. It's important you catch
   every thing and any thing that puts them at risk as a result of this code. If you see something
   in the code files but is not part of this pull request, feel free to point that out in the
   general issue comment.

   Common Security Issues (but not limited to):
   * Insecure Storage of Sensitive Data: Storing passwords, API keys, or other confidential
     information in plain text or easily reversible formats.
   * Injection Attacks: Failing to sanitize or validate user input, leaving the application
     vulnerable to SQL injection, command injection, or cross-site scripting (XSS).
   * Insufficient Access Controls: Not properly restricting access to sensitive data or
     functionalities.
   * Cross-Site Request Forgery (CSRF): Not protecting against CSRF attacks, which could allow
     an attacker to trick a user into performing unwanted actions.
   * Insecure Direct Object References (IDOR): Allowing users to directly access resources (e.g.,
     files, database records) without proper authorization checks.

5. Miscellaneous: Here are slough of other topics we'd like you to consider when reviewing the
   pull request. Note that for these, it might be best to summarize suggestions for these in the
   general pull request issue comment, but use your judgment if it should instead be its own
   review comment. Also, not all of these may apply to the codebase / pull request.
   a. Testing: Are there adequate unit tests, integration tests, or end-to-end tests? Do the tests
      cover edge cases and potential failure scenarios?
   b. Performance: Does the code meet performance requirements under expected load? Are there any
      obvious bottlenecks that could be improved?
   c. Scalability: Will the code be able to handle a growing user base or increased data volume?
   d. Modularity and Reusability: Is the code well-organized into modules or components that can
      be reused in other parts of the project?
   e. Error Logging and Monitoring: Are errors logged effectively, and are there mechanisms in
      place to monitor the application's health in production?
