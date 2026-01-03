def test_imports():
    """Basic smoke test that key libraries import successfully."""
    import importlib
    for pkg in ("pandas", "sqlalchemy"):
        mod = importlib.import_module(pkg)
        assert mod is not None
