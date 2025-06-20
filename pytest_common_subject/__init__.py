from importlib.metadata import version

from .exceptions import DeferredCommonSubjectRvalUsage
from .fixtures import precondition_fixture
from .mixins import (
    CommonSubjectTestMixin,
    AsyncCommonSubjectTestMixin,
    WithCommonSubjectDeferred,
)

__version__ = version('pytest-common-subject')

__all__ = [
    'DeferredCommonSubjectRvalUsage',
    'precondition_fixture',
    'CommonSubjectTestMixin',
    'AsyncCommonSubjectTestMixin',
    'WithCommonSubjectDeferred',
]
