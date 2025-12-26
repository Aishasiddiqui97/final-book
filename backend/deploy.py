"""Deployment script for the RAG Chatbot backend."""
import os
import sys
import subprocess
import argparse
from pathlib import Path


def install_dependencies():
    """Install required Python dependencies."""
    print("Installing Python dependencies...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                          cwd=".", capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error installing dependencies: {result.stderr}")
        return False

    print("Dependencies installed successfully")
    return True


def setup_environment():
    """Verify environment setup."""
    print("Verifying environment setup...")

    # Check for required files
    required_files = [
        "requirements.txt",
        ".env",  # We'll warn if missing but not fail
        "src/api/main.py"
    ]

    for file in required_files:
        if not Path(file).exists():
            if file == ".env":
                print(f"Warning: {file} not found. Please create it with required environment variables.")
            else:
                print(f"Error: Required file {file} not found.")
                return False

    # Check environment variables
    required_env_vars = [
        "OPENAI_API_KEY",
        "QDRANT_URL",
        "QDRANT_API_KEY"
    ]

    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your environment or .env file before running the server.")

    print("Environment setup verified")
    return True


def run_migrations():
    """Run any necessary setup/migrations."""
    print("Running setup tasks...")

    # Initialize vector database if needed
    try:
        from src.config.vector_db import vector_db_config
        print("Initializing vector database...")
        vector_db_config.create_collection()
        print("Vector database initialized")
    except Exception as e:
        print(f"Warning: Could not initialize vector database: {e}")
        print("Make sure your Qdrant credentials are correct.")

    return True


def start_server():
    """Start the server."""
    print("Starting the RAG Chatbot server...")

    try:
        from start_server import main as start_main
        start_main()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        return False

    return True


def deploy_local():
    """Deploy locally for development/testing."""
    print("Deploying locally...")

    if not setup_environment():
        return False

    if not install_dependencies():
        return False

    if not run_migrations():
        return False

    return start_server()


def deploy_production():
    """Deploy to production (placeholder)."""
    print("Production deployment steps would go here...")
    print("This would typically involve:")
    print("1. Building a Docker container")
    print("2. Pushing to a container registry")
    print("3. Deploying to a cloud platform")
    print("4. Setting up monitoring and logging")

    # For now, just do the same as local deployment
    return deploy_local()


def main():
    parser = argparse.ArgumentParser(description='Deploy the RAG Chatbot backend')
    parser.add_argument('environment', choices=['local', 'production'],
                       help='Deployment environment')
    parser.add_argument('--setup-only', action='store_true',
                       help='Run setup only, don\'t start server')

    args = parser.parse_args()

    print(f"Starting {args.environment} deployment...")

    if not setup_environment():
        print("Environment setup failed. Exiting.")
        return 1

    if not install_dependencies():
        print("Dependency installation failed. Exiting.")
        return 1

    if not run_migrations():
        print("Setup/migration failed. Exiting.")
        return 1

    if args.setup_only:
        print("Setup completed successfully. Server not started due to --setup-only flag.")
        return 0

    if args.environment == 'local':
        success = deploy_local()
    else:
        success = deploy_production()

    if success:
        print(f"{args.environment.title()} deployment completed successfully!")
        return 0
    else:
        print(f"{args.environment.title()} deployment failed!")
        return 1


if __name__ == "__main__":
    exit(main())