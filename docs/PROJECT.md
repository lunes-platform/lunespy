# Project Structure Guide[¹](#reference)

    lunespy/
    │   ├── client/
    │   │   ├── wallet/
    │   │   └──transaction/
    │   │       ├── cancel_lease/
    │   │       ├── transfer/
    │   │       ├── reissue/
    │   │       ├── issue/
    │   │       ├── lease/
    │   │       ├── alias/
    │   │       ├── lunex/
    │   │       ├── mass/
    │   │       └── burn/
    │   │
    │   ├── server/
    │   │   ├── transactions/
    │   │   ├── address/
    │   │   ├── blocks/
    │   │   └── nodes/
    │   │
    │   └── utils/
    │       └── crypto/
    |
    ├── tests/
    │   ├── client/
    │   │   └── wallet/
    │   │       └── .../
    │   │   └── transaction/
    │   │       └── .../
    │   │
    │   ├── server/
    │   │   └── .../
    │   │
    │   └── utils/
    │       └── .../
    |
    ├── data/
    │   ├── rich_list.json
    │   ├── tx-hash.json
    │   └── wallet.json
    │
    |
    ├── docs/
    │   ├── TUTORIAL.md
    │   └── PROJECT.md
    │
    ├── CHANGELOG.md
    ├── CONTRIBUTING.md
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    └── requeriments.txt
---

## Reference
¹ [Python Application Layouts: A Reference](https://realpython.com/python-application-layouts/)

