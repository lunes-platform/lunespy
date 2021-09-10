# Project Structure Guide[¹](#reference)

    lunespy/
    │   ├── client/
    │   │   ├── wallet/
    │   │   ├── issue_transaction/
    │   │   ├── leasing_transaction/
    │   │   ├── transfer_transaction/
    │   │   └── ...transaction/
    │   │
    │   ├── server/
    │   │   ├── address/
    │   │   ├── blocks/
    │   │   ├── transactions/
    │   │   └── .../
    │   │
    │   └── utils/
    │       ├── crypto/
    │       └── .../
    |
    ├── tests/
    │   ├── client/
    │   │   └── .../
    │   │
    │   ├── server/
    │   │   └── .../
    │   │
    │   └── utils/
    │       └── .../
    |
    ├── data/
    │   ├── info.log
    │   ├── all_wallets.csv
    │   └── rich_list.csv
    │
    |
    ├── docs/
    │   ├── CHANGELOG.md
    │   ├── CONTRIBUTING.md
    │   ├── TUTORIAL.md
    │   └── PROJECT.md
    |
    │
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    └── requeriments.txt
---

## Reference
¹ [Python Application Layouts: A Reference](https://realpython.com/python-application-layouts/)

