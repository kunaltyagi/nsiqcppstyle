import sys

import pytest

from nsiqcppstyle_exe import Filter

@pytest.fixture
def simple_filter():
    yield Filter("simple_test", {}, {})

@pytest.mark.skipif(sys.version_info < (3, 13), reason="Needs new glob features from 3.13")
def test_non_recursive_exclude(simple_filter: Filter):
    simple_filter.AddExclude("*.py")
    assert not simple_filter.CheckFileInclusion("hello.py")
    assert simple_filter.CheckFileInclusion("SomeDir/hello.py")

@pytest.mark.skipif(sys.version_info < (3, 13), reason="Needs new glob features from 3.13")
def test_recursive_exclude(simple_filter: Filter):
    simple_filter.AddExclude("**/*.py")
    assert not simple_filter.CheckFileInclusion("hello.py")
    assert not simple_filter.CheckFileInclusion("SomeDir/hello.py")

def test_prefix_match(simple_filter: Filter):
    simple_filter.AddExclude("test/")
    assert simple_filter.CheckFileInclusion("test.py")
    assert not simple_filter.CheckFileInclusion("test/test.py")
    assert not simple_filter.CheckFileInclusion("test/hello.py")

    simple_filter.AddInclude("test/test")
    assert simple_filter.CheckFileInclusion("test/test.py")
    assert not simple_filter.CheckFileInclusion("test/hello.py")
