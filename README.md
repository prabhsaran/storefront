# Storefront Project

This is a simple product catalog and filtering system built with Django. The web-app renders a single html page with description, category, and tags filters and entire list of products by default. The user can search for products based on these filters and view the filtered results. The project also includes a customized Django admin interface for managing products, categories, and tags. Project is built based on requirements provided in [this pdf](docs/requirements.pdf)

## Getting Started

### Prerequisites
- **Python 3.12.7** or higher [Download Python 3.12.7](https://www.python.org/downloads/release/python-3127/)
- **pipenv** for virtual environment and package management [Install pipenv](https://pipenv.pypa.io/en/latest/)

### Project Structure
```
storefront \
├── storefront (project)          
└── store (app)
└── db.sqlite3 (database) Note: This db is only included with the repository for easy setup and testing.
```              

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/prabhsaran/storefront
   cd storefront
   ```
2. **Install dependencies**:
   ```bash
   pipenv install
   ```
3. **Run the development server**:
    ```bash
    python manage.py runserver 8000
    ```
4. **Access the application**:
    - Open a browser and go to  http://localhost:8000/store/products/ to view the product search.
    - Go to http://localhost:8000/admin/ to access the Django admin interface with the following credentials:
        - Username: `admin`
        - Password: `admin`
        - Note: Credentials are only included for easy setup and testing.

### Running Tests
This project includes a basic test for the main search functionality. To run tests:
```bash
python manage.py test store
```
Django will set up a temporary test database, run all tests, and report results. No changes will affect the db.sqlite3 database.


### Assumptions and Additional Notes
 #### Alternate Project Structure
 Tags and Categories could be created as separate apps. This approach could make the project more modular and future-proof, especially if tags or categories become reusable across other future apps. However, all models were kept within the store app for simplicity, as this meets the current project scope and avoids additional complexity.

 #### Tooling
 Due to the small scope of the project, no additional tooling was setup. However, for production projects, tools like `black` for code formatting, `flake8` for linting, and `isort` for import sorting should be used to maintain code quality and consistency.


