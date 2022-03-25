from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models.aggregates import Aggregate

from .mixins import OrderableAggMixin

__all__ = [
    'ArrayAgg', 'BitAnd', 'BitOr', 'BoolAnd', 'BoolOr', 'JSONBAgg', 'StringAgg',
]


class ArrayAgg(OrderableAggMixin, Aggregate):
    function = 'ARRAY_AGG'
    template = '%(function)s(%(distinct)s%(expressions)s %(ordering)s)'

    @property
    def output_field(self):
        return ArrayField(self.source_expressions[0].output_field)

    def __init__(self, expression, distinct=False, **extra):
        super().__init__(expression, distinct='DISTINCT ' if distinct else '', **extra)

    def convert_value(self, value, expression, connection):
        if not value:
            return []
        return value


class BitAnd(Aggregate):
    function = 'BIT_AND'


class BitOr(Aggregate):
    function = 'BIT_OR'


class BoolAnd(Aggregate):
    function = 'BOOL_AND'


class BoolOr(Aggregate):
    function = 'BOOL_OR'


class JSONBAgg(Aggregate):
    function = 'JSONB_AGG'
    output_field = JSONField()

    def convert_value(self, value, expression, connection):
        if not value:
            return []
        return value


class StringAgg(OrderableAggMixin, Aggregate):
    function = 'STRING_AGG'
    template = "%(function)s(%(distinct)s%(expressions)s, '%(delimiter)s'%(ordering)s)"

    def __init__(self, expression, delimiter, distinct=False, **extra):
        distinct = 'DISTINCT ' if distinct else ''
        super().__init__(expression, delimiter=delimiter, distinct=distinct, **extra)

    def convert_value(self, value, expression, connection):
        if not value:
            return ''
        return value
