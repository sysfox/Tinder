"""Root pytest configuration: display docstrings as test names instead of file paths."""


def pytest_collection_modifyitems(items):
    """Replace each test's technical node ID with the first line of its docstring."""
    for item in items:
        doc = getattr(item.function, "__doc__", None)
        if doc:
            first_line = doc.strip().split("\n")[0].strip()
            if first_line:
                item._nodeid = first_line
