# NeonLush

NeonLush project - Django REST Framework based web application

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd neonlush.co
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install required packages

```bash
pip install -r requirements.txt
```

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

Enter username, email, and password when prompted.

### 8. Start the development server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

**Last updated:** July 6, 2025
**Maintainer:** selamet