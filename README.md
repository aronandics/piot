# Piot

Piot can be used for testing programs in any language that accept files as input.<br>
It's name stands for **P**rogram, **i**nput, **o**utput **t**est: it takes input files, passes them as arguments to a program, then compares the output to expectations.

## Installation

Download the repository and extract it wherever you like.<br>
The script is written in python and requires no further setup, provided that you have a working python environment. If not, please [install python](https://www.python.org/downloads/) first.

## Usage

- Create a directory named `tests` (preferably at the root of your project, but it's not a necessity)
- Inside `tests`, create input files for anything you want to test
- Create the corresponding files with the expected outputs, naming them `<name_of_test>.out`<br>
For example, the expected output file for `test.py` should be `test.out`

> input files without extensions are allowed, but two input files with the same name are **not**

After setting this up, navigate to the parent directory of `tests` (this may be the root directory of your project), and execute the following command adapted to your needs:

```
python path/to/piot.py program optional arguments
```

> Piot may be run with any version of python

For example, to test a python script in a POSIX-compatible environment, you may use:

```
python3 ~/piot/piot.py python3 script.py
```

> the program provided as argument is executed on your system, DO **NOT** PASS COMMANDS THAT MAY CAUSE DAMAGE

---

It may be useful to make your tests depend on each other. This way, the ones that are guaranteed to fail will be skipped. Dependencies can easily be specified by adding a `.dependencies` file to your `tests` directory with the following syntax:
```
dependent: required1, required2
```

Any number of requirements can be specified for one dependent, separated by commas, and any number of dependencies can be specified, separated by newlines.

> names of tests must be written **without** extensions

## Limitations

- if a test's name is included in `.dependencies`, it must **not** contain a space, a colon, or a comma
- tests with an extensionless input file cannot have periods in their names
- Piot cannot be used for testing programs that never return without interruption