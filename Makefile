# Makefile for the Nine project

.PHONY: run test clean help

# Default target
help:
	@echo "Nine - A program exploring the number 9"
	@echo ""
	@echo "Available commands:"
	@echo "  make run    - Run the nine program"
	@echo "  make test   - Run the test suite"
	@echo "  make clean  - Clean up temporary files"
	@echo "  make help   - Show this help message"

# Run the main program
run:
	@python3 nine.py

# Run tests
test:
	@python3 test_nine.py

# Clean up temporary files
clean:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@echo "Cleaned temporary files"