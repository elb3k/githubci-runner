import yaml
from typing import List, Dict


class Step:
    def __init__(self, name:str, cmd:str, envs:Dict[str, str]):
        self.name = name.strip()
        self.cmds = [ x.strip() for x in cmd.strip().split("\n") ] 
        self.envs = envs


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
            envs = step["env"] if "env" in step else dict()
            steps.append(Step(name=step_name, cmd=cmd, envs=envs))
        
        jobs[job_name] = Job(name=job_name, steps=steps)
        
    return jobs


