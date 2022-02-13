# CONTRIBUTING


## What is the workflow?

1. Create and describe your **proposal/bug** in an _issue_.
2. Create a new **branch** and **merge request** with the pattern `1-my-feature`.
3. Commit your code to the commit convention.
4. Finaly, update the **CHANGELOG** and **version** with:

```py
poetry run log
```

---

## Convention of Commits and Semantic Version

### **Commit Structure**

```
type(escope): short description

What does the modification do?
why was it modified?

#issue
```

### **Types**

- **deprecated!** compatibility break
- **merged** solve a problem and merge in `main`
- **added** adds a new feature
- **fixed** fixes a bug
- **removed** remove a peace of code
- **refactored** does not add a feature or fix a bug

### **Semantic Version**

- **deprecated!** -> _Major_
- **merged** -> _Minor_
- **added, fixed** -> _Patch_

---

## References

- [Good Practices](https://bestpractices.coreinfrastructure.org/pt-BR)
- [Semantic Versioning](https://semver.org/lang/pt-BR/)
- [More about Versioning](http://www.modelcvs.org/versioning/)
- [Versioning Automate](https://bhuwanupadhyay.github.io/2020/04/applying-semantic-versioning-with-git-repository/)
- [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0-beta.2/#why-use-conventional-commits)
- [Default Angular Commit](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)
- [Global hook for repositories](https://docs.gitlab.com/ce/administration/server_hooks.html#set-a-global-server-hook-for-all-repositories)
- [More about Commits](https://chris.beams.io/posts/git-commit/)
- [Quick Actions for Commits](https://docs.gitlab.com/ee/user/project/quick_actions.html)
- [Commits examples](https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/edit#)
- [Full Tutorial Add Convetional Commit as default](https://prahladyeri.com/blog/2019/06/how-to-enforce-conventional-commit-messages-using-git-hooks.html)
- [Create a global git commit hook](https://coderwall.com/p/jp7d5q/create-a-global-git-commit-hook)
