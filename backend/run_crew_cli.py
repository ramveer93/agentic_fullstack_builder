import sys
import os

# Ensure the src directory is in the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from agentic_fullstack_builder.crew import EngineeringTeam
from agentic_fullstack_builder.tools.sandbox_tools import reset_sandbox

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_crew_cli.py <requirements>")
        sys.exit(1)
        
    requirements = sys.argv[1]
    inputs = {'requirements': requirements}
    
    print("Resetting sandbox...")
    reset_sandbox()
    
    # Write a default README
    readme_content = """# Generated App

## How to run
1. Ensure you have `uv` installed.
2. Run `uv run app.py`
3. Open your browser to the URL printed in the terminal.
"""
    with open("sandbox/README.md", "w") as f:
        f.write(readme_content)
    
    print(f"Starting Crew with requirements:\n{requirements}")
    try:
        EngineeringTeam().crew().kickoff(inputs=inputs)
        print("Crew finished successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
