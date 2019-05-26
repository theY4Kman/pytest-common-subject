from types import ModuleType
from typing import Union

import pytest
from pytest_lambda.impl import LambdaFixture

__all__ = ['precondition_fixture']


def precondition_fixture(*args, **kwargs):
    """Fixture to be evaluated before the Common Subject is invoked

    NOTE: this fixture only makes sense when using CommonSubjectTestMixin, or
          its subclasses.

    Usage:

        class TestMyStuff(CommonSubjectTestMixin):
            common_subject = static_fixture(datetime.utcnow)
            before = precondition_fixture(lambda: datetime.utcnow())

            def it_evaluates_precondition_before_subject(self, common_subject_rval, before):
                assert before < common_subject_rval

    """
    return PreconditionFixture(*args, **kwargs)


class PreconditionFixture(LambdaFixture):
    def contribute_to_parent(self, parent: Union[type, ModuleType], name: str, **kwargs):
        # Add precondition marker to class. CommonSubjectTestMixin.marked_preconditions
        # will load all fixtures named by this marker.
        pytest.mark.precondition(name)(parent)

        return super().contribute_to_parent(parent, name, **kwargs)
