# Contributing

## What is the workflow?

1 - Create and describe your proposal in an [issue](https://github.com/Lunes-platform/LunesPy/issues/new/choose)

2 - Create a new branch with o pattern `isse/MY_NEW_FEATURE`

3 - Create a new [pull request](https://github.com/Lunes-platform/LunesPy/compare) for add your changes in `main` branch

4 - Write tests for your code

5 - Commit your code using we coventional commit

6 - Write a docs for your changes

7 - Finally, update the CHANGELOG  



## Conventional Commit and Semmantic Version

- **[Major] deprecated**: modification that breaks compatibility
- **[Minor] issued**: resolve any issue
- **[Patch] added**: adds a new feature
- **[Patch] fixed**: fixes a bug
- **changed**: does not add a feature or fix a bug
- **removed**: feature removed
- **security**: in the case of vulnerabilities


## How to generate Changelog

```py
poetry run log
```
