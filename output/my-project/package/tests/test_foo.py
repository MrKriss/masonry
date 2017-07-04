
import ss
import pytest


def test_foo_does_x():

    assert False

def test_foo_does_y():

    assert False


# -------- #
# Examples #
# -------- #

# Tesing Exceptions 
# ---------------------------------------------------

# import pytest
# def f():
#     raise SystemExit(1)

# def test_mytest():
#     with pytest.raises(SystemExit):
#         f()

# Fixtures
# -----------------------------------------------------------

# import pytest

# @pytest.fixture
# def smtp():
#     import smtplib
#     return smtplib.SMTP("smtp.gmail.com")

# def test_ehlo(smtp):
#     response, msg = smtp.ehlo()
#     assert response == 250
#     assert 0 # for demo purposes


# Monkey Patching
# ------------------------------------------------------------------

# import os.path
# def getssh(): # pseudo application code
#     return os.path.join(os.path.expanduser("~admin"), '.ssh')

# def test_mytest(monkeypatch):
#     def mockreturn(path):
#         return '/abc'
#     monkeypatch.setattr(os.path, 'expanduser', mockreturn)
#     x = getssh()
#     assert x == '/abc/.ssh'

# Parameterising tests
# -----------------------------------------------------------------------

# import pytest
# @pytest.mark.parametrize("test_input,expected", [
#     ("3+5", 8),
#     ("2+4", 6),
#     ("6*9", 42),
# ])
# def test_eval(test_input, expected):
#     assert eval(test_input) == expected