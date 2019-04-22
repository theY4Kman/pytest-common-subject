import pkg_resources

from .exceptions import DeferredCommonSubjectRvalUsage
from .fixtures import precondition_fixture
from .mixins import CommonSubjectTestMixin, WithCommonSubjectDeferred

__version__ = pkg_resources.get_distribution('pytest-common-subject').version

__all__ = [
    'DeferredCommonSubjectRvalUsage',
    'precondition_fixture',
    'CommonSubjectTestMixin',
    'WithCommonSubjectDeferred',
]
