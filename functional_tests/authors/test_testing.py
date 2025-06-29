from functional_tests.base import BaseWebDriverForFunctionalTests


class TestTesting(BaseWebDriverForFunctionalTests):
    def test_the_test(self):
        assert 1 == 2
