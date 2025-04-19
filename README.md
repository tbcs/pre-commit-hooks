# A collection of pre-commit hooks

This repository contains Git hook definitions for use with
[pre-commit](http://pre-commit.com/).

## List of hooks

### Style checkers / formatters

| id             | name                                                                                      |
| -------------- | ----------------------------------------------------------------------------------------- |
| style-java     | Check/fix Java style ([google-java-format](https://github.com/google/google-java-format)) |
| style-json     | Check/fix JSON style ([prettier](https://github.com/prettier/prettier))                   |
| style-kotlin   | Check/fix Kotlin style ([ktfmt](https://github.com/facebook/ktfmt))                       |
| style-markdown | Check/fix Markdown style ([prettier](https://github.com/prettier/prettier))               |
| style-php      | Check/fix PHP style ([prettier](https://github.com/prettier/plugin-php))                  |
| style-shell    | Check/fix shell style ([shfmt](https://github.com/mvdan/sh))                              |
| style-xml      | Check/fix XML style ([xmllint](http://xmlsoft.org/xmllint.html))                          |
| style-yaml     | Check/fix YAML style ([prettier](https://github.com/prettier/prettier))                   |

### Linters

| id                                     | name                                                          |
| -------------------------------------- | ------------------------------------------------------------- |
| lint-shell                             | Lint shell scripts ([ShellCheck](https://www.shellcheck.net)) |
| lint-makefile-suspicious-continuations | Check Makefiles for suspicious continuations                  |
| lint-makefile-suspicious-indents       | Check Makefiles for suspicious indents                        |

### Commit message preparation and linting

| id                 | name                                                                                      |
| ------------------ | ----------------------------------------------------------------------------------------- |
| commit-msg-check   | Check commit message ([commitlint](https://github.com/conventional-changelog/commitlint)) |
| commit-msg-restore | Restore previously rejected commit message                                                |

## Configuration of pre-commit

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/tbcs/pre-commit-hooks
    rev: "20250419105518.29bc9a8d"
    hooks:
      - id: style-java
      - id: commit-msg-restore
      - id: commit-msg-check
```

## Configuration of specific hooks

### commitlint

The following example file `.commitlintrc.yml` demonstrates the configuration
required for using the `commitlint` hook. Note that the Node modules listed in
`extends` must be referenced by their full path in this hook collection's Docker
image.

```yaml
---
# ------------------------------------------------------------------------------
# Configuration for commitlint, extending the conventional commits shared
# configuration:
# https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional
# ------------------------------------------------------------------------------

scope-list: &scope-list
  - PLACEHOLDER_SCOPE_TO_REJECT_INVALID_SCOPES
type-list: &type-list ## conventional commit types
  - chore
  - ci
  - feat
  - fix
  - docs
  - style
  - refactor
  - perf
  - test
  - revert
  ## custom types
  # - cfg
extends: ["/usr/local/lib/node_modules/@commitlint/config-conventional"]
rules:
  scope-enum: [2, always, *scope-list]
  type-enum: [2, always, *type-list]
```
