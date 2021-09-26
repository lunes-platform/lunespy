# Contributing

## What is the workflow?

1 - Create and describe your proposal in an [issue](https://github.com/Lunes-platform/LunesPy/issues/new/choose)

2 - Create a new branch with o pattern `feature/MY_FEATURE` or `fix/MY_BUG`

3 - Write your tests BEFORE your code, PULL REQUESTS WITHOUT TEST WILL BE REJECTED

4 - Commit your code using we coventional commit, COMMITS OUTSIDE THE CONVENTIONAL WILL BE REJECTED

5 - Write a docs for your changes, PULL REQUESTS WITHOUT DOCS WILL BE REJECTED

6 - Generete a new CHANGELOG with yours commit using the script python below 

7 - Commit your change and create a new [pull request](https://github.com/Lunes-platform/LunesPy/compare) for add your changes in `main` branch


## Conventional Commit and Semmantic Version

- **[Major] deprecated**: modification that breaks compatibility
- **[Minor] issued**: resolve any issue
- **[Patch] added**: adds a new feature
- **[Patch] fixed**: fixes a bug
- **changed**: does not add a feature or fix a bug
- **removed**: feature removed
- **security**: in the case of vulnerabilities


## How to generate Changelog

Save this script below as `script.py` 
and run `python3 scrip.py`

```py
from os import remove, system as sys
from datetime import datetime, timedelta

def generate_logs():
    sys('git log --pretty="- [%h](%H) %s [%ai]" > ./logs.txt')

def read_logs() -> list:
    with open('./logs.txt', 'r') as file:
        logs = file.readlines()

    remove("./logs.txt")
    return logs


def edit_logs(logs: list) -> list:
    range_date = {}
    for line in logs:
        range_date[line[-27:-17]] = []
        for commit in logs:
            if line[-27:-17] == commit[-27:-17]:
                range_date[line[-27:-17]].append(commit)

    changelog = ['# Changelog\n']
    for date in range_date.keys():
        changelog.append(f"\n## {date}\n")
        for commit in range_date[date]:
            edited_commit = commit[:-29] + '\n'
            changelog.append(edited_commit)
    
    return changelog

def save_changelog(changelog: list):
    with open('./docs/CHANGELOG.md', 'w') as file:
        file.writelines(changelog)


generate_logs()
logs = read_logs()
changelog = edit_logs(logs)
save_changelog(changelog)
```
