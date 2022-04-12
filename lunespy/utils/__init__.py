def flat_map(listOfLists):
    from itertools import chain
    return list(chain.from_iterable(listOfLists))

# def semantic_version() -> str:
#     from subprocess import check_output

#     def get_logs() -> list[str]:
#         return check_output(
#             'git log --pretty="%s"',
#             shell=True
#         ).decode().split('\n')[::-1]

#     major, minor, patch = 0,0,0

#     for commit in get_logs():
#         commit_type = commit.split(":")[0]
#         match commit_type:
#             case "deprecated!":
#                 patch = 0
#                 minor = 0
#                 major += 1
#             case "Merge" | "issued" | "merged" | "add" | "added":
#                 patch = 0
#                 minor += 1
#             case "fixed" | "fix" | "Update":
#                 patch += 1
#     print(
#         bcolors.OKGREEN + f"v{major}.{minor}.{patch}" + bcolors.ENDC
#     )
#     return f"v{major}.{minor}.{patch}"


# def changelog(length=0):
#     from subprocess import check_output

#     deprecated = ["## Deprecated"]
#     merged_issued = ["## Issued"]
#     added = ["## Added"]
#     fixed = ["## Fixed"]
#     refactored = ["## Refactored"]
#     removed = ["## Removed"]
#     other = ["## Others"]
#     changelog = [
#         [f"# Changelog {semantic_version()}"],
#         deprecated, merged_issued, added, fixed, refactored, removed, other
#     ]

#     def get_logs() -> list[str]:
#         if length != 0:
#             return check_output(
#                 'git log --pretty="- [%h](%H) %s"',
#                 shell=True
#             ).decode().split('\n')[:length]
#         else:
#             return check_output(
#                 'git log --pretty="- [%h](%H) %s"',
#                 shell=True
#             ).decode().split('\n')

#     for commit in get_logs():
#         commit_type = commit.split(":")[0].split(" ")[-1]
#         match commit_type:
#             case "deprecated!" | "deprecated":
#                 deprecated.append(commit)
#             case "Merge" | "issued" | "merged":
#                 merged_issued.append(commit)
#             case "add" | "added":
#                 added.append(commit)
#             case "fixed" | "fix" | "Update":
#                 fixed.append(commit)
#             case "refactored" | "refact":
#                 refactored.append(commit)
#             case "remove" | "removed":
#                 removed.append(commit)
#             case _:
#                 other.append(commit)

#     with open('./CHANGELOG.md', 'w') as file:
#         for line in flat_map(changelog):
#             file.write(line + "\n")


def now() -> int:
    from time import time

    return int(
        time() * 1000
    )
