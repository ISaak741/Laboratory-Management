# 🚀 Laboratory Management

## 🛠️ Quick Start

Follow these steps to set up the project on your local machine.

### 1. Clone & Environment Setup

# Clone the repository

git clone git@github.com:ISaak741/Laboratory-Management.git
cd Laboratory-Management

# Create virtual environment

python3 -m venv venv

# Activate venv

# On Windows: venv\Scripts\activate

# On Mac/Linux: source venv/bin/activate

### 2. Install Dependencies

pip3 install -r requirements.txt

### 3. Configure Environment Variables

Create a `.env` file in the root directory. You will need a secure secret key for Flask.

**Generate your secret key using this command:**
python -c 'import secrets; print(secrets.token_hex())'

**Create a .env file and paste your generated key:**
FLASK_APP=app.py
FLASK_DEBUG=1
SECRET_KEY=your_generated_token_here
SQLALCHEMY_DATABASE_URI=sqlite:///site.db

### 4. Database Setup

Since migrations are tracked in this repo, you don't need to run `init`. Simply run the upgrade command to generate your local database file:
flask db upgrade

### 5. Run the Server

flask run

---

## 📂 Project Structure

├── controllers/ # Create Blueprints here; they load automatically
├── models/ # Define Mapped models here
├── migrations/ # Database version control (DO NOT DELETE)
├── instance/ # Local SQLite database (git-ignored)
├── bootstrap.py # The "Brain" - handles dynamic discovery
└── app.py # Entry point

## 🤝 Adding New Features

### To Add a Route:

Simply create a new .py file in controllers/. Define a Blueprint object within that file, and the bootstrap.py logic will register it automatically on the next restart.

### To Add a Model:

1. Create a new .py file in models/.
2. Define your class using the Mapped and mapped_column syntax.
3. Generate and apply the migration:
   flask db migrate -m "Added new model"
   flask db upgrade
