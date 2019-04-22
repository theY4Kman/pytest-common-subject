from typing import Type

from lazy_object_proxy import Proxy


class VolatileValue(Proxy):
    """Special object which raises on any attempt to utilize it

    An instance of this class is returned from the `common_subject_rval`
    fixture when `is_common_subject_deferred` is set to True. This is to warn
    the user early of unintended usages, which could possibly lead to false
    negatives (passing tests that should be failing).
    """

    def __init__(self,
                 message: str = 'An attempt to use a VolatileValue was made',
                 exc_class: Type[Exception] = RuntimeError):

        def factory():
            raise exc_class(message)

        super().__init__(factory)

