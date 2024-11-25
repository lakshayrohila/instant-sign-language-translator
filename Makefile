SRC_DIR := $(PWD)
TMP_DIR := $(shell mktemp -d)

live_test: 4_live_test.py
	@echo "Creating temporary directory..."
	@cp "$(SRC_DIR)/4_live_test.py" "$(TMP_DIR)/live_test.py"
	@cd "$(TMP_DIR)" && \
	echo "Compiling Python script with Cython..." && \
	cython live_test.py --embed && \
	echo "Detecting Python version..." && \
	PYTHON_LIB_VER=python$$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')$$(python3-config --abiflags) && \
	echo "Building executable with GCC..." && \
	gcc -O3 $$(python3-config --includes) live_test.c -o live_test $$(python3-config --ldflags) -l$${PYTHON_LIB_VER} && \
	echo "Moving executable to source directory..." && \
	mv live_test "$(SRC_DIR)/"
	@echo "Cleaning up temporary directory..."
	@rm -rf "$(TMP_DIR)"

.PHONY: live_test
