from crlat_siteserve_client.constants import *
from crlat_siteserve_client.siteserve_client import query_builder, simple_filter
from tests import s


# PoolForClass
# '?simpleFilter=pool.provider:in:P,E,A,H,V'
# '&simpleFilter=pool.isActive:isTrue'
# '&simpleFilter=pool.type:in:{type}'
query = query_builder()\
    .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.PROVIDER, OPERATORS.IN, 'P,E,A,H,V'))\
    .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE))\
    .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.IN, '232'))

s.ss_pool_for_class(class_id='3233', query_builder=query)
