# Setup

## 1. Create virtual environment

python -m venv venv

## 2. Activate virtual environment

### Linux / Mac
source venv/bin/activate

### Windows
venv\Scripts\activate

## 3. Install dependencies

pip install -r requirements.txt

## 4. Configure environment variables

Create a `.env` file in the project root:

WIKI_USER_AGENT=YourProjectName/0.1 (your_email@example.com)
REQUEST_SLEEP=0.5

## 5. Run the project

python main.py