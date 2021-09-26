# Project Structure Guide[¹](#reference)

    lunespy/
    │   ├── client/
    │   │   ├── wallet/
    │   │   └──transaction/
    │   │       ├── transfer/
    │   │       ├── lease/
    │   │       ├── issue/
    │   │       ├── reissue/
    │   │       ├── alias/
    │   │       ├── burn/
    │   │       └── .../
    │   │
    │   ├── server/
    │   │   ├── address/
    │   │   ├── blocks/
    │   │   ├── transactions/
    │   │   └── .../
    │   │
    │   └── utils/
    │       ├── crypto/
    │       ├── settings/
    │       └── .../
    |
    ├── tests/
    │   ├── client/
    │   │   ├── wallet/
    │   │   └──transaction/
    │   │       ├── transfer/
    │   │       ├── lease/
    │   │       ├── issue/
    │   │       ├── reissue/
    │   │       ├── alias/
    │   │       └── burn/
    │   │
    │   ├── server/
    │   │   └── .../
    │   │
    │   └── utils/
    │       └── .../
    |
    ├── data/
    │   ├── transaction-XYZ.json
    │   ├── wallet.json
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

