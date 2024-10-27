import pytest

from nsiqcppstyle_exe import Filter


@pytest.fixture
def simple_filter():
    return Filter("simple_test", {}, {})


def test_non_recursive_exclude(simple_filter: Filter):
    simple_filter.AddExclude("*.py")
    assert not simple_filter.CheckFileInclusion("hello.py")
    assert simple_filter.CheckFileInclusion("SomeDir/hello.py")
    assert simple_filter.CheckFileInclusion("ParentDir/SomeDir/hello.py")

    simple_filter.AddExclude("*/*.py")
    assert not simple_filter.CheckFileInclusion("SomeDir/hello.py")
    assert simple_filter.CheckFileInclusion("ParentDir/SomeDir/hello.py")


def test_recursive_exclude(simple_filter: Filter):
    simple_filter.AddExclude("**/*.py")
    assert not simple_filter.CheckFileInclusion("hello.py")
    assert not simple_filter.CheckFileInclusion("SomeDir/hello.py")
    assert not simple_filter.CheckFileInclusion("ParentDir/SomeDir/hello.py")


def test_mix_exclude(simple_filter: Filter):
    simple_filter.AddExclude("test/**/*.py")
    assert simple_filter.CheckFileInclusion("hello.py")
    assert not simple_filter.CheckFileInclusion("test/hello.py")
    assert not simple_filter.CheckFileInclusion("test/SomeDir/hello.py")


def test_prefix_match(simple_filter: Filter):
    simple_filter.AddExclude("test/")
    assert simple_filter.CheckFileInclusion("test.py")
    assert not simple_filter.CheckFileInclusion("test/test.py")
    assert not simple_filter.CheckFileInclusion("test/hello.py")

    simple_filter.AddInclude("test/test")
    assert simple_filter.CheckFileInclusion("test/test.py")
    assert not simple_filter.CheckFileInclusion("test/hello.py")
