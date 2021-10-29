from argparse import ArgumentParser
from githubci_runner.config import load_config
from githubci_runner.runner import run_job
from termcolor import cprint
import subprocess

def get_shell(name):
    p = subprocess.Popen(f"which {name}", shell=True, stdout=subprocess.PIPE)
    out, _ = p.communicate()
    return out.decode("ascii").strip(), p.returncode == 0


def parse_args():
    parser = ArgumentParser()

    parser.add_argument("--ci-path", type=str, default="./.github/workflows/ci.yml", help="Path of ci file")
    parser.add_argument("-j", "--job-name", type=str, required=True, help="Specify which job to run")
    parser.add_argument("--start-step", type=str, default=None, help="Start with specified step, default = start from the beginning")
    parser.add_argument("-s", "--sleep", type=int, default=0, help="Additional sleep option in between steps")
    parser.add_argument("--shell", type=str, default="bash", help="Which shell to use run commands")
    parser.add_argument("-v", "--verbose", action="store_true")

    return parser.parse_args()


def main():
    args = parse_args()

    # Load config
    jobs = load_config(args.ci_path, verbose=args.verbose)
    
    if args.job_name not in jobs:
        cprint(f"Job <{args.job_name}> not found", "red", attrs=["bold"])
        return
    
    # Get Shell
    shell, ok = get_shell(args.shell)
    if not ok:
        cprint(f"Invalid shell: {args.shell}", "red", attrs=["bold"])
        return
    
    
    # Run jobs
    run_job(jobs[args.job_name], shell, start_step=args.start_step, additional_sleep=args.sleep, verbose=args.verbose)



if __name__ == "__main__":
    main()