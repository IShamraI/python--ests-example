PROTO_DIR = proto
PROTO_FILES = $(wildcard $(PROTO_DIR)/*.proto)
PYTHON_OUT_DIR = .

VENV_NAME = venv
VENV_DIR = $(PWD)/$(VENV_NAME)
PIP = $(VENV_DIR)/bin/pip
PYTHON = $(VENV_DIR)/bin/python

.PHONY: all clean env proto pip-upgrade install test

all: env pip-upgrade install proto

test: proto
	@echo "Running tests with pytest..."
	@$(PYTHON) -m pytest tests/test_example_grpc.py

env:
	@echo "Creating Python virtual environment..."
	@python3 -m venv $(VENV_DIR)

proto: $(PROTO_FILES)
	@echo "Generating Python files from Protocol Buffers..."
	@$(PYTHON) -m grpc_tools.protoc -I$(PROTO_DIR) --python_out=$(PYTHON_OUT_DIR) --grpc_python_out=$(PYTHON_OUT_DIR) $(PROTO_FILES)

pip-upgrade:
	@echo "Upgrade pip to the latest"
	@$(PYTHON) -m pip install --upgrade pip

install:
	@echo "Installing dependencies..."
	@$(PIP) install -r requirements.txt
	@$(PIP) install --upgrade grpcio


clean:
	@echo "Cleaning generated files..."
	@rm -f $(PYTHON_OUT_DIR)/*_pb2.py $(PYTHON_OUT_DIR)/*_pb2_grpc.py
	@echo "Cleaning virtual environment..."
	@rm -rf $(VENV_DIR)
