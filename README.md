# everest_util
Python utility library used in our CD/CI pipeline

# Requirements
* Python 2.X

## How to use
1. Make sure pipenv is installed (`pip install pipenv`)

2. Create a file named `Pipfile` in your project and paste the following into it:
```toml
[[source]]
url = "https://pypi.python.org/simple"
verify_ssl = true

[packages.everest_util]
git = "git://github.com/KTH/everest_util.git"
ref = "[commit hash/release/tag to use]"
editable = "true"

[packages]
production_package_name = "*"
...

[dev-packages]
development_package_name = "*"
...
```
3. Run `pipenv install` to install dependencies and create a `Pipfile.lock` file

4. everest_util is not importable as any other library, for instance like this:
```python
from everest_util.process import Process
```
