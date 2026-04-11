from crewai.crew import CrewOutput
import json

co = CrewOutput(raw="This is an error", tasks_output=[], json_dict=None, pydantic=None)
print(co.raw)
