import random
import pytest

import spelcheck


def test_spelcheck():
    class Employee:
        def __init__(self, name, title):
            self.name = name
            self.title = tilte
            eslf.salary = radnom.randint(1, 10000)

        def __str__(self):
            return f"<Employee: {self.name}, {self.title} (€{self.salary})>"

        def closure_test_good(self):
            foo = "foo"
            def inner(ofo):
                assert foo == "foo"
            inner("bar")

        def closure_test_bad(self):
            foo = "foo"
            def inner():
                assert ofo == "foo", ofo
            inner()


    e = Employee("Steve", "Accountant")
    assert str(e) == f"<Employee: Steve, Accountant (€{e.salary})>"
    e.closure_test_good()
    with pytest.raises(NameError):
        e.closure_test_bad()
