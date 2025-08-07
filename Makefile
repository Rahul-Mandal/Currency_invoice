# Makefile for Invoice Validator & Currency Converter Microservice

# Python virtual environment setup
VENV_NAME = venv
PYTHON = python3
PIP = pip
VENV_ACTIVATE = $(VENV_NAME)/Scripts/activate

# Install dependencies
install:
	$(PYTHON) -m venv $(VENV_NAME)
	. $(VENV_ACTIVATE) && $(PIP) install --upgrade pip
	. $(VENV_ACTIVATE) && $(PIP) install -r requirements.txt

# Run the FastAPI server locally
run:
	. $(VENV_ACTIVATE) && uvicorn app.main:app --reload

# Run tests (example with pytest)
test:
	. $(VENV_ACTIVATE) && pytest tests/

# Lint the code using flake8
lint:
	. $(VENV_ACTIVATE) && flake8 app/ tests/

# Format code using black
format:
	. $(VENV_ACTIVATE) && black app/ tests/

# Clean the virtual environment
clean:
	rm -rf $(VENV_NAME)

# Install pre-commit hooks (example)
precommit:
	. $(VENV_ACTIVATE) && pre-commit install

# Run all steps in one
ci: lint test format

