# main.py
"""
CLI entry point for the ReAct agent.
"""
import sys
from react_agent import run_agent
from tools import TOOLS

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <your question>")
        return
    query = " ".join(sys.argv[1:])
    print(f"User: {query}\n---")
    try:
        answer = run_agent(query, TOOLS)
        print(f"Agent: {answer}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
