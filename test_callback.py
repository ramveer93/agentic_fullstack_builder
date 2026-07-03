from crewai import Agent, Task, Crew
import json

def step_cb(step):
    print(f"STEP: {type(step)}")
    print(dir(step))

agent = Agent(role="Researcher", goal="Test", backstory="Test", verbose=False, step_callback=step_cb)
task = Task(description="Calculate 2+2", expected_output="4", agent=agent)
Crew(agents=[agent], tasks=[task], verbose=False).kickoff()
