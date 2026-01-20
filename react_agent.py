# react_agent.py
"""
ReAct agent core logic, following the required pseudo-code structure.
"""
from tools import TOOLS
from llm import llm

class Action:
    def __init__(self, took, tool=None, argument=None):
        self.took = took  # 'finish' or 'tool'
        self.tool = tool
        self.argument = argument
    def __repr__(self):
        return f"Action(took={self.took}, tool={self.tool}, argument={self.argument})"

def build_prompt(query, history, tools):
    tool_desc = "\n".join(f"- {name}: {fn.__doc__}" for name, fn in tools.items())
    hist = ""
    for i, (action, result) in enumerate(history):
        hist += f"Step {i+1}:\nThought: {action.took}\nAction: {action.tool}({action.argument})\nObservation: {result}\n"
    prompt = f"""
You are an expert assistant for art, books, coffee, and matcha. You can use tools or answer directly. 
Available tools:\n{tool_desc}\n
User question: {query}\n
{hist}Respond with either:
- Action: <tool>(<argument>)
- Finish: <final answer>
"""
    return prompt.strip()

def parse_action(response):
    response = response.strip()
    if response.lower().startswith("finish:"):
        return Action("finish", argument=response[len("finish:"):].strip())
    if response.lower().startswith("action:"):
        # Parse Action: tool(argument)
        import re
        m = re.match(r"Action:\s*(\w+)\((.*)\)", response, re.I)
        if m:
            tool, arg = m.group(1), m.group(2)
            return Action("tool", tool=tool, argument=arg)
    # fallback: treat as finish
    return Action("finish", argument=response)

def execute_tool(tool, argument):
    fn = TOOLS.get(tool)
    if not fn:
        return f"Unknown tool: {tool}"
    try:
        return fn(argument)
    except Exception as e:
        return f"Tool error: {e}"

def run_agent(query, tools, max_steps=100):
    history = []
    for step in range(max_steps):
        prompt = build_prompt(query, history, tools)
        response = llm.complete(prompt)
        action = parse_action(response)
        if action.took == "finish":
            return action.argument
        result = execute_tool(action.tool, action.argument)
        history.append((action, result))
    return "Max steps reached"
