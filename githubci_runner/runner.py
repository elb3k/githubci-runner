import subprocess
from time import sleep
from githubci_runner.config import *
from bash import bash
from termcolor import cprint

def run_cmd(cmd:str, verbose:bool):
    stderr = subprocess.PIPE
    stdout = subprocess.PIPE
    if verbose:
        stderr = subprocess.STDOUT
        stdout = None
    return bash(cmd, stderr=stderr, stdout=stdout)
  
       

def run_step(step: Step, verbose:bool) -> bool:

    cprint(f">> {step.name}", 'yellow', end='\r' if not verbose else '\n')
    try:
        ret = run_cmd(step.cmd, verbose)
        if not verbose:
            if ret.code != 0:
                print("\n".join(ret.stdout))
            else:
                cprint(f">> {step.name}", 'green')
        return ret.code == 0
    except Exception as e:
        print(e)
        return False

def run_job(job: Job, start_step:str = None, additional_sleep:int = 0, verbose:bool=False) -> None:
    cprint(f"> Starting job: {job.name}", 'blue', attrs=['bold'])

    if len(job.steps) == 0:
        cprint(f"No steps in this job", "red", attrs=["bold"])
        return
    
    additional_sleep = max(additional_sleep, 0)
    
    if start_step is None:
        index = 0
    else:
        start_step = start_step.strip()
        for idx, step in enumerate(job.steps):
            if step.name == start_step:
                index = idx
                break
    
    for step in job.steps[index:]:
        if not run_step(step, verbose):
            cprint(f"Failed at step <{step.name}>: {step.cmd}", "red", attrs=["bold"])
            return
        
        sleep(additional_sleep)



