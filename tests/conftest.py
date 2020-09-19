def pytest_addoption(parser):
    parser.addoption("--source_dir", action="store", default="/Users/kobarhan/workspace/gitsy")
    parser.addoption("--test_dir", action="store", default="/Users/kobarhan/workspace/gitsy_test")
