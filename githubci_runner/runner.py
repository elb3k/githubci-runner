import subprocess
from time import sleep
from githubci_runner.config import *
# from bash import bash
from subprocess import Popen
from termcolor import cprint
from typing import Dict
import os

def eval_envs(envs: Dict[str, str]) -> Dict[str, str]:
    os_envs = os.environ.copy()

    for name, val in envs.items():
        if name not in envs:
            os_envs[name] = val
    
    return os_envs

def run_cmd(cmd:str, shell: str, verbose:bool, env: Dict[str, str]):
    stderr = subprocess.PIPE
    stdout = subprocess.PIPE
    if verbose:
        stderr = subprocess.STDOUT
        stdout = None
    p = Popen(cmd, stderr=stderr, stdout=stdout, shell=shell, executable=shell, env=env)

    out, _ = p.communicate()
    return p.returncode, out


def run_step(step: Step, shell: str, verbose:bool) -> bool:

    cprint(f">> {step.name}", 'yellow', end="".join(['\r'] * len(step.name.split('\n'))) if not verbose else '\n')
    try:
        envs = eval_envs(step.envs)
        for cmd in step.cmds:
            ret_code, out = run_cmd(cmd, shell, verbose, envs)
            if not verbose:
                if ret_code != 0:
                    print("\n".join(out))
                else:
                    cprint(f">> {step.name}", 'green')
            if ret_code != 0:
                return False
        
        return True
    except Exception as e:
        print(e)
        return False

def run_job(job: Job, shell:str, start_step:str = None, additional_sleep:int = 0, verbose:bool=False) -> None:
    cprint(f"> Starting job: {job.name}", 'blue', attrs=['bold'])

    if len(job.steps) == 0:
        cprint(f"No steps in this job", "red", attrs=["bold"])
        return
    
    additional_sleep = max(additional_sleep, 0)
    
    index = -1
    if start_step is None:
        index = 0
    else:
        start_step = start_step.strip()
        for idx, step in enumerate(job.steps):
            if step.name == start_step:
                index = idx
                break
    if index == -1:
        cprint(f"No step found <{start_step}>", "red", attrs=["bold"])
        return
    
    for step in job.steps[index:]:
        if not run_step(step, shell, verbose):
            cprint(f"Failed at step <{step.name}>: {step.cmds}", "red", attrs=["bold"])
            return
        
        sleep(additional_sleep)
    
    cprint(f"Successfully finished job: {job.name}", "green", attrs=["bold"])



