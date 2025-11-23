#!/usr/bin/env python3
"""
CLI Deployment Script for Greeter Agent
This script automates the deployment of the greeter agent to IBM Watsonx Orchestrate.
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        if check:
            sys.exit(1)
        return e

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("Checking prerequisites...")
    
    # Check Python version
    python_version = sys.version_info
    if not (python_version.major == 3 and 11 <= python_version.minor <= 13):
        print(f"ERROR: Python 3.11-3.13 required, found {python_version.major}.{python_version.minor}")
        sys.exit(1)
    print(f"✓ Python version: {python_version.major}.{python_version.minor}")
    
    # Check if orchestrate CLI is available
    result = run_command(["orchestrate", "--version"], check=False)
    if result.returncode != 0:
        print("ERROR: 'orchestrate' CLI not found. Install with: pip install --upgrade ibm-watsonx-orchestrate")
        sys.exit(1)
    print("✓ Orchestrate CLI found")
    
    # Check required files
    required_files = ["greeter.yaml", "greeter_tools.py", "requirements.txt"]
    for file in required_files:
        if not Path(file).exists():
            print(f"ERROR: Required file not found: {file}")
            sys.exit(1)
        print(f"✓ Found {file}")
    
    print("All prerequisites met!\n")

def setup_environment(env_name, service_url, api_key=None):
    """Set up the orchestrate environment."""
    print(f"Setting up environment: {env_name}")
    
    # Check if environment already exists
    result = run_command(["orchestrate", "env", "list"], check=False)
    if env_name in result.stdout:
        print(f"Environment '{env_name}' already exists. Activating...")
        run_command(["orchestrate", "env", "activate", "--name", env_name])
    else:
        # Create new environment
        cmd = ["orchestrate", "env", "add", 
               "--name", env_name,
               "--url", service_url,
               "--type", "ibm_iam",
               "--activate"]
        
        if api_key:
            # Some CLI versions support --api-key flag
            cmd.extend(["--api-key", api_key])
        
        run_command(cmd)
    
    print("✓ Environment configured\n")

def import_agent(yaml_file):
    """Import agent from YAML file."""
    print(f"Importing agent from {yaml_file}...")
    run_command(["orchestrate", "agents", "import", "-f", yaml_file])
    print("✓ Agent imported\n")

def upload_tools(agent_name, tools_file):
    """Upload tools file to the agent."""
    print(f"Uploading tools file: {tools_file}...")
    
    # Try different command formats
    cmd = ["orchestrate", "agents", "update", "--name", agent_name, "--tools-file", tools_file]
    result = run_command(cmd, check=False)
    
    if result.returncode != 0:
        # Try alternative command
        cmd = ["orchestrate", "agents", "tools", "upload", "--name", agent_name, "--file", tools_file]
        result = run_command(cmd, check=False)
    
    if result.returncode == 0:
        print("✓ Tools uploaded\n")
    else:
        print("WARNING: Could not upload tools file. It may have been included in the import.\n")

def deploy_agent(agent_name):
    """Deploy the agent."""
    print(f"Deploying agent: {agent_name}...")
    run_command(["orchestrate", "agents", "deploy", "--name", agent_name])
    print("✓ Agent deployed\n")

def verify_deployment(agent_name):
    """Verify the agent deployment."""
    print("Verifying deployment...")
    
    # Get agent details
    result = run_command(["orchestrate", "agents", "get", "--name", agent_name], check=False)
    if result.returncode == 0:
        print(result.stdout)
        print("✓ Agent verification complete\n")
    else:
        print("WARNING: Could not verify agent details\n")

def main():
    parser = argparse.ArgumentParser(
        description="Deploy greeter agent to IBM Watsonx Orchestrate via CLI"
    )
    parser.add_argument("--env-name", required=True, help="Environment name")
    parser.add_argument("--service-url", required=True, help="Watsonx Orchestrate service URL")
    parser.add_argument("--api-key", help="IBM Cloud API key (optional, will prompt if not provided)")
    parser.add_argument("--agent-name", default="greeter", help="Agent name (default: greeter)")
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("Greeter Agent - CLI Deployment Script")
    print("=" * 60)
    print()
    
    # Check prerequisites
    check_prerequisites()
    
    # Setup environment
    setup_environment(args.env_name, args.service_url, args.api_key)
    
    # Import agent
    import_agent("greeter.yaml")
    
    # Upload tools (may be included in import, but try anyway)
    upload_tools(args.agent_name, "greeter_tools.py")
    
    # Deploy agent
    deploy_agent(args.agent_name)
    
    # Verify deployment
    verify_deployment(args.agent_name)
    
    print("=" * 60)
    print("Deployment Complete!")
    print("=" * 60)
    print(f"\nAgent '{args.agent_name}' has been deployed to Watsonx Orchestrate.")
    print("\nNext steps:")
    print("1. Test the agent: orchestrate agents chat --name greeter --message 'Greeting'")
    print("2. Check agent status: orchestrate agents get --name greeter")
    print("3. View agent logs in the Watsonx Orchestrate UI")
    print("4. Start the server: python server.py")

if __name__ == "__main__":
    main()

