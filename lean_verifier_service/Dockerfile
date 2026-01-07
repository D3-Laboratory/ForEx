# Use a single-stage build for simplicity
FROM python:3.10-slim-bookworm

# Install system dependencies for elan (Lean's toolchain manager) and lake
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    libgmp-dev \
    && rm -rf /var/lib/apt/lists/*

# Install elan
ENV ELAN_HOME="/usr/local/elan"
ENV PATH="${ELAN_HOME}/bin:${PATH}"
RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain none

# Set up the main application directory for the Python server
WORKDIR /app

# Copy Python server requirements and the server script itself
COPY lean_verifier_service/requirements.txt ./
COPY lean_verifier_service/api_server.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the directory for the Lean project, as expected by the api_server
RUN mkdir -p /app/repl
WORKDIR /app/repl

# Copy the local Lean project files into the container
COPY lean_verifier_service/lean-toolchain ./
COPY lean_verifier_service/lakefile.lean ./
COPY lean_verifier_service/lake-manifest.json ./
COPY lean_verifier_service/ToolTest01.lean ./

# Install the specified Lean toolchain and build the Lean project
# This ensures that 'lake' and its dependencies (like mathlib) are ready.
RUN elan toolchain install $(cat lean-toolchain)
RUN elan default $(cat lean-toolchain)
RUN lake build

# Switch back to the Python server's directory
WORKDIR /app

# Expose the port the server will run on
EXPOSE 6789

# Command to run the API server
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "6789"]
