from typing import Callable

import pytest
from pytest_lambda import lambda_fixture, static_fixture

from pytest_common_subject import (
    CommonSubjectTestMixin,
    DeferredCommonSubjectRvalUsage,
    precondition_fixture,
    WithCommonSubjectDeferred,
)


class DescribeCommonSubjectTestMixin:

    @pytest.fixture
    def get_next_val(self) -> Callable[[], int]:
        """Method returning a higher number each invocation per test
        """
        counter = 0

        def get_next_val() -> int:
            nonlocal counter
            counter += 1
            return counter

        return get_next_val


    class TestIsCommonSubjectDeferred(CommonSubjectTestMixin):
        common_subject = lambda_fixture('get_next_val')

        class AssertNotDeferred:
            """Test context mixin verifying traits of an undeferred common_subject
            """
            def it_calls_common_subject_automatically(self, call_common_subject):
                expected = 2  # it ought to have already been called once,
                              # so we get value #2 when calling it below
                actual = call_common_subject()
                assert expected == actual

            def it_allows_usage_of_common_subject_rval(self, common_subject_rval):
                assert common_subject_rval == common_subject_rval


        class AssertDeferred:
            """Test context mixin verifying traits of n deferred common_subject
            """
            def it_does_not_call_common_subject_automatically(self, call_common_subject):
                expected = 1  # it ought not to have been called,
                              # so we get value #1 when calling it below
                actual = call_common_subject()
                assert expected == actual

            def it_disallows_usage_of_common_subject_rval(self, common_subject_rval):
                with pytest.raises(DeferredCommonSubjectRvalUsage):
                    assert common_subject_rval == common_subject_rval


        class ContextNotDeferred(AssertNotDeferred):
            is_common_subject_deferred = static_fixture(False)


        class ContextDeferred(AssertDeferred):
            is_common_subject_deferred = static_fixture(True)


        class ContextDeferredByMixin(
            WithCommonSubjectDeferred,
            AssertDeferred,
        ):
            pass


    class TestPreconditions(CommonSubjectTestMixin):

        # This essentially causes the common_subject_rval fixture to invoke this method
        common_subject = lambda_fixture('get_next_val')


        class TestOverridingPreconditionsFixture:
            # Grab a val at the beginning
            first_val = lambda_fixture(lambda get_next_val: get_next_val())

            # Grab a val late (but should still be before common_subject_rval!)
            late_val = pytest.mark.late(lambda_fixture(lambda get_next_val: get_next_val()))

            preconditions = lambda_fixture('first_val', 'late_val')

            def it_evaluates_preconditions_before_invoking_subject(self, common_subject_rval, first_val, late_val):
                assert first_val < late_val < common_subject_rval


        class TestPreconditionMark:
            # Grab a val at the beginning
            first_val = lambda_fixture(lambda get_next_val: get_next_val())

            # Grab a val late (but should still be before common_subject_rval!)
            late_val = pytest.mark.late(lambda_fixture(lambda get_next_val: get_next_val()))

            @pytest.mark.precondition('first_val')
            @pytest.mark.precondition('late_val')
            def it_evaluates_preconditions_before_invoking_subject(self, common_subject_rval, first_val, late_val):
                assert first_val < late_val < common_subject_rval


        class TestPreconditionFixture:
            # Grab a val at the beginning
            first_val = precondition_fixture(lambda get_next_val: get_next_val())

            # Grab a val late (but should still be before common_subject_rval!)
            late_val = pytest.mark.late(precondition_fixture(lambda get_next_val: get_next_val()))

            def it_evaluates_preconditions_before_invoking_subject(self, common_subject_rval, first_val, late_val):
                assert first_val < late_val < common_subject_rval
