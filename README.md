# Github CI local runner
Simple tool for running github ci.yaml jobs

## Installation:
```bash
pip install git+https://github.com/elb3k/githubci-runner
```

## Sample usage:
```bash
githubci-runner --ci-path .github/workflows/ci.yaml -j unit-tests --start-step "Set up Postgres" -v
```

## Arguments:
1. `--ci-path` - path to `ci.yml` file (default `.github/workflows/ci.yml`)
2. `-j` - specified job name inside config file
3. `--start-step` - start from the custom step (sometimes you want to skip github specific steps), if not specified start from the beginning
4. `-s` - sleep `X` seconds in between steps
5. `--shell` - which shell to use to run commands, default bash
6. `-v` - for verbose operation

## TODOs
1. Include environmental variables - currently not supported, but processed will grab system-wide environmental variables.
2. Automatically skip `github-actions` - currently you have to specify exact step, to skip steps.