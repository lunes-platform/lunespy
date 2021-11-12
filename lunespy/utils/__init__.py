def export_dict(path: str, name: str, dict: dict) -> bool:
    import json
    
    full_path = f"{path}/{name}"
    with open(full_path, 'w') as file:
        file.write(json.dumps(dict))


def generate_log() -> None:
    from subprocess import check_output

    def get_logs() -> list:
        return check_output(
            'git log --pretty="- [%h](%H) %s [%ai]"',
            shell=True
        ).decode().split('\n')
    
    def logs_to_changelog(logs: list) -> list:
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

    def save_changelog(changelog: list) -> None:
        with open('./docs/CHANGELOG.md', 'w') as file:
            file.writelines(changelog)

    save_changelog(
        logs_to_changelog(
            get_logs()
            )
    )


def now() -> int:
    from time import time

    return int(
        time() * 1000
    )
