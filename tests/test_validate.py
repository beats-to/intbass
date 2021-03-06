from nose.tools import eq_, raises
import unittest
from app import validate
import bcrypt


class TestEmail(unittest.TestCase):
    def test_valid(self):
        eq_(validate.email('example@example.com'), 'example@example.com')

    def test_validnumbers(self):
        eq_(validate.email('example123@example.com'), 'example123@example.com')

    def test_normalisedomain(self):
        eq_(validate.email('example@eXample.cOm'), 'example@example.com')

    def test_leavelocalpart(self):
        eq_(validate.email('eXample@eXample.cOm'), 'eXample@example.com')

    def test_punycode(self):
        eq_(validate.email('example@xn--bcher-kva.ch'),
            'example@xn--bcher-kva.ch')

    def test_shortdomain(self):
        eq_(validate.email('example@c.je'),
            'example@c.je')

    @raises(validate.ValidationError)
    def test_invalid(self):
        validate.email('example')

    @raises(validate.ValidationError)
    def test_nolocalpart(self):
        validate.email('@example.com')

    @raises(validate.ValidationError)
    def test_nodomain(self):
        validate.email('example@')

    @raises(validate.ValidationError)
    def test_domainallwrong(self):
        validate.email('example@a')

    @raises(validate.ValidationError)
    def test_invaliddomain(self):
        validate.email('example@a.a')

    @raises(validate.ValidationError)
    def test_domainnodot(self):
        validate.email('example@aaaaaaaaaaa')


class TestUsername(unittest.TestCase):
    def test_valid(self):
        eq_(validate.username('perfect'), 'perfect')

    @raises(validate.ValidationError)
    def test_blank(self):
        validate.username('')

    @raises(validate.ValidationError)
    def test_tooshort(self):
        validate.username('ex')


class TestPassword(unittest.TestCase):
    def test_valid(self):
        password = validate.password('perfect')
        assert bcrypt.hashpw('perfect', password) == password

    @raises(validate.ValidationError)
    def test_blank(self):
        validate.password('')
