from importlib import metadata

from .exceptions import DeferredCommonSubjectRvalUsage
from .fixtures import precondition_fixture
from .mixins import (
    CommonSubjectTestMixin,
    AsyncCommonSubjectTestMixin,
    WithCommonSubjectDeferred,
)

try:
    __version__ = metadata.version('pytest-only')
except metadata.PackageNotFoundError:
    __version__ = 'dev'


__all__ = [
    'DeferredCommonSubjectRvalUsage',
    'precondition_fixture',
    'CommonSubjectTestMixin',
    'AsyncCommonSubjectTestMixin',
    'WithCommonSubjectDeferred',
]
