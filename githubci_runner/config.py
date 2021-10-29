import yaml
from typing import List

import os, sys

# class Verbose:
#     def __init__(self, verbose):
#         self.verbose = verbose
#     def __enter__(self):
#         if not self.verbose:
#             self._original_stdout = sys.stdout
#             sys.stdout = open(os.devnull, 'w')

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if not self.verbose:
#             sys.stdout.close()
#             sys.stdout = self._original_stdout

class Step:
    def __init__(self, name:str, cmd:str):
        self.name = name.strip()
        self.cmds = [ x.strip() for x in cmd.strip().split("\n") ] 


class Job:
    def __init__(self, name:str, steps:List[Step]):
        self.name = name.strip()
        self.steps = steps

def load_yaml(filename):
    with open(filename, "r") as f:
        cfg = yaml.safe_load(f)
        return cfg
        


def load_config(filename, verbose=False):
   
    cfg = load_yaml(filename)
    # Extract Jobs:
    jobs = {}
    for job_name, job in cfg.get("jobs", {}).items():
        if "name" not in job or "steps" not in job:
            continue
            
        steps = []
        # Extract steps
        for step in job["steps"]:
            if "run" not in step:
                continue
            cmd = step["run"]
            step_name = step["name"] if "name" in step else cmd
            steps.append(Step(name=step_name, cmd=cmd))
        
        jobs[job_name] = Job(name=job_name, steps=steps)
        
    return jobs


