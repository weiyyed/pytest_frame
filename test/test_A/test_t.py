import pytest

@pytest.fixture()
def user():
    print("获取用户名")
    a = "yoyo"
    return a

def test_1(user):
    assert user == "yoyo"
def test_2():
    assert 1