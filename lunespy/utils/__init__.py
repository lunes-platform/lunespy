import json

def export_dict(path: str, name: str, dict: dict) -> bool:
    full_path = f"{path}/{name}"
    with open(full_path, 'w') as file:
        file.write(json.dumps(dict))

def generate_log():        
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
        with open('./CHANGELOG.md', 'w') as file:
            file.writelines(changelog)


    generate_logs()
    logs = read_logs()
    changelog = edit_logs(logs)
    save_changelog(changelog)