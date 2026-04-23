# Contributing to LexHarmoni

Thank you for your interest in contributing to LexHarmoni! We welcome all contributions that help improve regulatory analysis.

## Development Setup

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally.
3.  **Backend setup**:
    ```bash
    cd backend
    python -m venv venv
    .\venv\Scripts\activate # Windows
    pip install -r requirements.txt
    ```
4.  **Frontend setup**:
    ```bash
    cd frontend
    npm install
    ```

## Branching & Commits

-   **Branch Naming**:
    -   `feat/` for new features
    -   `fix/` for bug fixes
    -   `docs/` for documentation updates
    -   `refactor/` for code refactoring
-   **Commit Format**: We follow [Conventional Commits](https://www.conventionalcommits.org/).
    -   Example: `feat(api): add manifest endpoint`
-   **DCO (Developer Certificate of Origin)**:
    All commits must be signed off with `git commit -s`. This certifies that you have the right to submit the code under the Apache 2.0 license.

## Pull Request Process

1.  Create a branch for your changes.
2.  Ensure tests pass (if applicable).
3.  Submit a Pull Request targeting the `main` branch.
4.  A maintainer will review your PR.

## Coding Standards

-   **Python**: We use `ruff` for linting and formatting.
-   **TypeScript/React**: We use `eslint` and `prettier`.
-   **Testing**: New features should include unit tests where possible.

## License

By contributing, you agree that your contributions will be licensed under the [Apache License, Version 2.0](LICENSE).
