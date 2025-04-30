# LocalPythonCMS

![Screenshot](./assets/images/readme_logo.png)

A content management system (CMS) written in Python that allows you to create, edit, and publish web content

## Build Setup

```bash
# Arch Linux setup and required packages
$ sudo pacman -Syu
$ sudo pacman -S python-pip sqlite openssh upx
$ python -V && pip --version
$ git clone git@github.com:ncklinux/LocalPythonCMS.git
$ cd LocalPythonCMS
$ python -m venv .venv # Virtual environment (recommended)
$ pip install python-i18n pandas country_converter black pyinstaller requests PyQt6 PyYAML mypy flake8 bandit
$ git checkout -b YOUR_BRANCH_NAME

# Ubuntu setup and required packages
$ sudo apt update
$ sudo apt install python3-pip sqlite3 openssh-client upx python3.12-venv
$ python3 -V && pip3 --version
$ git clone git@github.com:ncklinux/LocalPythonCMS.git
$ cd LocalPythonCMS
$ python3 -m venv .venv # Virtual environment (recommended)
$ source .venv/bin/activate
$ pip3 install python-i18n pandas country_converter black pyinstaller requests PyQt6 PyYAML mypy flake8 bandit
$ git checkout -b YOUR_BRANCH_NAME

# Launch
$ python main.py

# Build for production
$ wget https://github.com/konstantinstadler/country_converter/blob/master/country_converter/country_data.tsv
# Another way it's to find the file and use the relative path to country_data.tsv e.g. --add-data '../.local/lib/python3.YOUR_VERSION/site-packages/country_converter/country_data.tsv' or, just copy country_data.tsv in LocalPythonCMS directory
# find / -type f -name "country_data.tsv" 2>&1 | grep -v 'Permission denied'
$ python -m PyInstaller --noconsole --onefile --windowed --exclude-module tkinter --add-data 'country_data.tsv:country_converter' main.py
# There are also some other options, like fbs (based on PyInstaller) or Flatpak
```

## Motivation

Empowering users to take control of their digital lives is the driving force behind my latest endeavor!

In an era where data breaches and security threats are rampant, I believe it's essential to prioritize local control and security, including [Ed25519](https://ed25519.cr.yp.to/) elliptic curve signature key pairs for connections, as suggested in the [Practical Cryptography with Go](https://leanpub.com/gocrypto/read#leanpub-auto-chapter-5-digital-signatures) book, data encryption and VPN (will be supported directly by the software), makes it great for many reasons! Most importantly, by hosting your Content Management System (CMS) on your own machine, you can ensure that your data remains yours, stored securely on your local computer, with automatic backups before every public commit of content. Yes, I'm referring to Git of course, you will be able to compare your local content with the uploaded version, which may give you information about something that was unknowingly changed.

This approach eliminates the need for constant online connectivity and reduces the risk of exposing sensitive information to potential threats. It's a simple yet effective solution that prioritizes security and privacy.

I've always believed that it's time to rethink our approach to CMS development. The '90s mindset of storing administrative interfaces alongside website content is no longer sufficient in today's landscape. It's time to adapt and innovate. By taking control of our own data and adopting more secure practices, we can all play a part in shaping a more secure online future.

Also, imagine having the power to update your website's content management system with ease, just like updating your favorite web browser. No more tedious tech jargon or complicated network configurations - just a seamless, hassle-free experience that lets you focus on what matters most: creating amazing content and connecting with your audience :wink:

John Johnson says _“First, solve the problem. Then, write the code.”_

| Result 01                                                | Result 02                                                |
| -------------------------------------------------------- | -------------------------------------------------------- |
| ![Screenshot](./assets/images/screenshot20240625_01.png) | ![Screenshot](./assets/images/screenshot20240625_02.png) |

## Internationalization

This project uses [python-i18n](https://pypi.org/project/python-i18n/) for translations, an out-of-the-box library for designing and developing software, so it can be adapted for users of different cultures and languages. The files are located in the [locales](https://github.com/ncklinux/LocalPythonCMS/tree/main/locales) directory in [YAML](https://yaml.org/) format. [JSON](https://www.json.org) format is also supported, to be used it must be specified explicitly `i18n.set('file_format', 'json')`

## SQLite

Start the [SQLite](https://sqlite.org/cli.html) program by typing `sqlite3` at the Terminal, followed by the name of the file that holds the database.

```bash
$ sqlite3 assets/sqlite/localpythoncms.sqlite

# SQLite CLI
sqlite> .tables
sqlite> select * from users;
```

![Screenshot](./assets/images/sqlite_screenshot_20221127.png)

## PEP8 & Black

This project follows the [PEP8](https://peps.python.org/pep-0008/) style, which provides guidelines and best practices for writing Python code, and [Black](https://github.com/psf/black) for formatting, that makes code review faster by producing the smallest diffs possible (it's already available for most editors and IDEs [VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter), [ST4](https://packagecontrol.io/packages/python-black), [PyCharm](https://plugins.jetbrains.com/plugin/14321-blackconnect) and also via [CLI](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html) e.g. `black {source_file_or_directory}`, to list all options use `black --help`).

If you use PyCharm but for whatever reason you don't want to use the [BlackConnect](https://plugins.jetbrains.com/plugin/14321-blackconnect) plugin and therefore [blackd](https://black.readthedocs.io/en/stable/usage_and_configuration/black_as_a_server.html), follow the screenshots below to set up [black](https://pypi.org/project/black/) as an external tool with a file watcher in order to run it on save. Use `which black` to identify the location of the executable and add it in the "Program" input field.

| IDE 01                                    | IDE 02                                    |
| ----------------------------------------- | ----------------------------------------- |
| ![Screenshot](./assets/images/ide_01.png) | ![Screenshot](./assets/images/ide_02.png) |

## Type Annotations

[Mypy](https://mypy-lang.org) is an optional static type checker for Python that aims to combine the benefits of dynamic (or "duck") typing and static typing. Mypy combines the expressive power and convenience of Python with a powerful type system and compile-time type checking. Mypy type checks standard Python programs; run them using any Python VM with basically no runtime overhead.

```bash
$ mypy --ignore-missing-imports main.py
# Success: no issues found in 1 source file
```

## Linting

Python linting, also known as code linting or static code analysis, is the process of analyzing Python code for potential errors, bugs, security and stylistic issues. The term "lint" comes from the idea of using a lint roller to remove tangled threads from fabric, and in this context, Python linting is like using a tool to "lint" or clean up your Python code to make it more readable, maintainable, and error-free.

- There are some linters out there, the most tried and tested is [Flake8](https://flake8.pycqa.org), "the wrapper which verifies pep8, pyflakes, and circular complexity", also has a low false positive rate.
- [Bandit](https://bandit.readthedocs.io/en/latest/) is a tool designed to find common security issues in Python code. To do this, Bandit processes each file, builds an AST from it, and runs appropriate plugins against the AST nodes. Once Bandit has finished scanning all the files, it generates a report.

## Troubleshooting

If you encountered the following module error, in fact, any similar module error `No module named 'pip'`, see below for more details:

```bash
$ python main.py

# Traceback (most recent call last):
#   File ".venv/bin/pip", line 5, in <module>
#     from pip._internal.cli.main import main
# ModuleNotFoundError: No module named 'pip'
```

It turns out that Virtualenv is not up to date, use the following commands to fix the problem:

```bash
$ deactivate
$ rm -rf .venv
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install ...
```

And reinstall all the PIP packages as you did at the [beginning](https://github.com/ncklinux/LocalPythonCMS?tab=readme-ov-file#build-setup) when you started with the program, then execute `python main.py` again, this time should work without module issues.

## License

GNU General Public License v3.0 - See the [LICENSE](https://github.com/ncklinux/LocalPythonCMS/blob/main/LICENSE) file in this project for details.

## Disclaimer

This project is distributed FREE & WITHOUT ANY WARRANTY. Report any bugs or suggestions as an [issue](https://github.com/ncklinux/LocalPythonCMS/issues/new).

## Contributing

Please read the [contribution](https://github.com/ncklinux/LocalPythonCMS/blob/main/.github/CONTRIBUTING.md) guidelines.

## Commit Messages

This repository follows the [Conventional Commits](https://www.conventionalcommits.org) specification, the commit message should never exceed 100 characters and must be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Note

I will keep and maintain this project as open source forever! [Watch it](https://github.com/ncklinux/LocalPythonCMS/subscription), give it a :star: and follow me on [GitHub](https://github.com/ncklinux) and [Twitter](https://twitter.com/ncklinux)

## Resources

Icons from [Google Material Symbols](https://fonts.google.com/icons)

## Powered by

<img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/unix/unix-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bash/bash-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/ssh/ssh-original-wordmark.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/qt/qt-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" />
