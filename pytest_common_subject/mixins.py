from typing import Callable, Any, TypeVar, Dict

import pytest

from .exceptions import DeferredCommonSubjectRvalUsage
from .util import VolatileValue

__all__ = [
    'CommonSubjectTestMixin',
    'WithCommonSubjectDeferred',
]

V = TypeVar('V')


class CommonSubjectTestMixin:
    """Abstract mixin for test contexts revolving around a common target

    Imperative tests are intensive to read. To grok what a test is *actually*
    trying to prove requires inspecting many lines of code which are ultimately
    inessential boilerplate.

    If, instead, we group our tests by the Subject being prodded, we can cordon
    off boilerplate to a single location, leaving only the juicy bits left to
    read.

    This mixin will call a single function for every test method, and provide
    its return value as a fixture, which is always evaluated after all other
    fixtures (so they can still be used for setup). The args passed in this
    function call can be customized by overriding the args/kwargs fixtures.

    Test contexts defined underneath this mixin are free to override
    args/kwargs, and create/override fixtures to setup the environment for the
    function call. This encourages named, well-defined contexts for testing
    the common subject from different viewpoints.

    This pattern also encourages slimmer tests, ideally responsible for testing
    a single aspect of the common subject and named descriptively. The upshot
    of this is all issues can be reported in one test run – as opposed to
    monolith tests, where fixing an issue and re-running the test suite reveals
    the next thing to fix.
    """

    @pytest.fixture
    def common_subject(self, *args) -> Callable[..., V]:
        """The method being tested in this context"""
        raise NotImplementedError(
            'Please override the `common_subject` fixture and provide a callable.')

    @pytest.fixture
    def is_common_subject_deferred(self) -> bool:
        """Whether to hold off on calling common_subject automatically

        If True, common_subject is not called in the `common_subject_rval`
        fixture. Instead, `common_subject_rval` will return a special DEFERRED
        value, which will raise an exception if an attempt is made to use the
        value — this is to aid in preventing unintended misuse.

        Deferring `common_subject_rval` is useful when one wishes to test
        whether `common_subject` raises an exception.

        Example:

            class DescribeMyErroneousMethod(
                CommonSubjectTestMixin
            ):
                common_subject = static_fixture(my_erroneous_method)
                is_common_subject_deferred = static_fixture(True)

                def it_raises_exception(self, call_common_subject):
                    with pytest.raises(MyException):
                        call_common_subject()

        See also the WithCommonSubjectDeferred test mixin
        """
        return False

    @pytest.fixture(autouse=True)
    @pytest.mark.late  # this ensures the fixture is executed at end of setup
                       # NOTE: this MUST be placed after pytest.fixture
    def common_subject_rval(self,
                            is_common_subject_deferred: bool,
                            call_common_subject: Callable[[], V],
                            all_preconditions: Any,
                            ) -> V:
        """The return value from invoking the common subject in this env

        To perform any post-processing on the return value (like parsing the
        JSON of an HTTP response), it's recommended to define another fixture
        that requests `common_subject_rval`.
        """
        if is_common_subject_deferred:
            return VolatileValue(
                'An attempt was made to use `common_subject_rval` while '
                '`is_common_subject_deferred` is True. This exception is '
                'thrown to prevent accidental passing of tests through '
                'unintended use of a deferred `common_subject_rval`',
                exc_class=DeferredCommonSubjectRvalUsage,
            )

        return call_common_subject()

    @pytest.fixture
    def call_common_subject(self,
                            common_subject: Callable[..., V],
                            args: tuple,
                            kwargs: Dict[str, Any],
                            ) -> Callable[[], V]:
        """A 0-arg method which invokes common_subject and returns its result

        Override this to customize how the common subject is invoked.
        """
        def call_common_subject() -> V:
            return common_subject(*args, **kwargs)
        return call_common_subject

    @pytest.fixture
    def args(self) -> tuple:
        """Inline arguments to be passed when invoking common_subject"""
        return ()

    @pytest.fixture
    def kwargs(self) -> dict:
        """Keyword arguments to be passed when invoking common_subject"""
        return {}

    @pytest.fixture
    def all_preconditions(self, preconditions: Any, marked_preconditions: Any):
        """Metafixture to request preconditions declared by any means

        Preconditions can be declared by overriding the `preconditions`
        fixture, using the @pytest.mark.precondition('fixture_name') marker,
        or by using the `precondition_fixture()` lambda fixture declaration.
        `all_preconditions` loads each of these types of preconditions.

        `common_subject_rval` requests `all_preconditions`, instead of directly requesting
        `preconditions` and `marked_preconditions`, so the user may customize
        precondition loading without having to completely redefine `common_subject_rval`.
        """

    @pytest.fixture
    def preconditions(self):
        """Any preconditions to be evaluated before the subject is invoked

        This fixture is requested by the common_subject_rval fixture, before calling
        call_common_subject(). By overriding this fixture, one can request
        other fixtures to be evaluated as "preconditions".

        Example:

            class TestMyStuff(CommonSubjectTestMixin):
                common_subject = lambda_fixture(lambda: MyModel.objects.all().delete())

                initial_count = lambda_fixture(lambda: MyModel.objects.count())
                preconditions = lambda_fixture('initial_count')

                def it_deletes_things(self, initial_count):
                    assert initial_count == 1
                    assert MyModel.objects.count() == 0

        """

    @pytest.fixture
    def marked_preconditions(self, request):
        """Load any fixtures declared with @pytest.mark.precondition('name')

        NOTE: this is how precondition_fixture() declares preconditions
        """
        precondition_marks = tuple(request.node.iter_markers('precondition'))
        precondition_fixtures = [mark.args[0] for mark in precondition_marks]

        for fixturename in precondition_fixtures:
            request.getfixturevalue(fixturename)


class WithCommonSubjectDeferred:
    """Test context mixin which sets `is_common_subject_deferred` to True

    This will defer the automatic calling of `common_subject`, leaving its
    invocation the responsibility of the user.
    """

    @pytest.fixture
    def is_common_subject_deferred(self) -> bool:
        return True
