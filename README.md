# spelcheck 🖊️👎✨🎉

    pip install spelcheck

Automagically spellcheck your classes. Definitely do this.

## Usage

After you've pip-installed it, just `import spelcheck` somewhere in your
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

If the autocorrection is too aggressive for you (or not aggressive enough) you
can set the minimum fuzzywuzzy score (default: 75) before defining any classes:

```python
import spelcheck
spelcheck.SPELCHECK_MINSCORE = 95  # be more precise
spelcheck.SPELCHECK_MINSCORE = 50  # be more aggressive
```

## Open issues

- [ ] Closures don't work. That is: we can't automatically correct a typo that
  should be a nonlocal name. I don't know if this is possible at all without
  changing our technique completely (maybe by parsing the source and looking at
  what function the inner function is defined in and what names exist there).
- [ ] Support Python 3.8. At the moment this doesn't seem to work in 3.8, I
  assume this is because of positional-only arguments which may have changed
  how a code object looks like. This seems doable.
