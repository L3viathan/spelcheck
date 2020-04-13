# spelcheck

    pip install spelcheck

Automagically spellcheck your classes. Definitely do this.

## Usage

After you've pip-installed it, just `import spellcheck` somewhere in your
project (ideally before you define any classes). Some magic will then occur,
and your typos will be fixed. Observe:

```python
>>> import random
>>> import spelcheck
>>> class Employee:
...     def __init__(self, name, title):
...         self.name = name
...         self.title = tilte  # oops, we misspelled "title"
...         eslf.salary = radnom.randint(1, 10000)  # damn, misspelled "random"
...
...     def __str__(self):
...         return f"<Employee: {self.name}, {self.title} (€{self.salary})>"

>>> e = Employee("Steve", "Accountant")
>>> print(e)
<Employee: Steve, Accountant (€4325)>
```
