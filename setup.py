#!/usr/bin/env python3
"""
Pinellone Game Setup Script
This script sets up the complete development environment for the Pinellone game.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def setup_backend():
    """Set up the Python backend."""
    print("\n=== Setting up Backend ===")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("Backend directory not found!")
        return False
    
    # Create virtual environment
    venv_path = backend_dir / "venv"
    if not venv_path.exists():
        print("Creating virtual environment...")
        run_command(f"{sys.executable} -m venv venv", cwd=backend_dir)
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        pip_path = venv_path / "Scripts" / "pip"
        python_path = venv_path / "Scripts" / "python"
    else:  # Unix-like
        pip_path = venv_path / "bin" / "pip"
        python_path = venv_path / "bin" / "python"
    
    print("Installing Python dependencies...")
    run_command(f"{pip_path} install -r requirements.txt", cwd=backend_dir)
    
    # Run tests
    print("Running backend tests...")
    run_command(f"{python_path} -m pytest tests/ -v", cwd=backend_dir, check=False)
    
    return True

def setup_frontend():
    """Set up the React frontend."""
    print("\n=== Setting up Frontend ===")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("Frontend directory not found!")
        return False
    
    # Install npm dependencies
    print("Installing npm dependencies...")
    run_command("npm install", cwd=frontend_dir)
    
    # Build frontend
    print("Building frontend...")
    run_command("npm run build", cwd=frontend_dir, check=False)
    
    return True

def create_env_files():
    """Create environment configuration files."""
    print("\n=== Creating Environment Files ===")
    
    # Backend .env
    backend_env = Path("backend/.env")
    if not backend_env.exists():
        backend_env.write_text("""# Pinellone Backend Configuration
DEBUG=True
LOG_LEVEL=DEBUG
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
""")
        print("Created backend/.env")
    
    # Frontend .env
    frontend_env = Path("frontend/.env")
    if not frontend_env.exists():
        frontend_env.write_text("""# Pinellone Frontend Configuration
VITE_API_URL=http://localhost:8000
VITE_DEBUG_MODE=true
""")
        print("Created frontend/.env")

def main():
    """Main setup function."""
    print("🎮 Pinellone Game Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("Error: Please run this script from the pinellone-modern directory")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("Backend setup failed!")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("Frontend setup failed!")
        sys.exit(1)
    
    # Create environment files
    create_env_files()
    
    print("\n" + "=" * 50)
    print("✅ Setup Complete!")
    print("\nTo start the game:")
    print("1. Start backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload")
    print("2. Start frontend: cd frontend && npm run dev")
    print("\nThen visit http://localhost:3000 to play!")

if __name__ == "__main__":
    main()