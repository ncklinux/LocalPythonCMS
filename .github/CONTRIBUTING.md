# Contributing guidelines

## General guidelines and philosophy

For those just getting started with pull requests, GitHub has a [how to](https://help.github.com/articles/using-pull-requests/).

- Always open an [issue](https://github.com/ncklinux/LocalPythonCMS/issues/new) first.
- Include unit tests when you contribute new features, as they help to:
  - Prove that your code works correctly.
  - Guard against future breaking changes to lower the maintenance cost.
- Bug fixes also generally require unit tests, because the presence of bugs usually indicates insufficient test coverage.
- Keep compatibility in mind when you do code changes.
- For full new features (e.g., a cutting-edge algorithm, or anything new) give please some airtime before a decision is made regarding whether they are to be merged to “base” branch.
- As each PR requires several unit tests, submitting a PR just to fix a typo, a warning, etc. is discouraged.
