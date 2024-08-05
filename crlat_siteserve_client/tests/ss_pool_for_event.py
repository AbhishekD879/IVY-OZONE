from crlat_siteserve_client.constants import *
from crlat_siteserve_client.siteserve_client import query_builder, simple_filter
from tests import s



# PoolForEvent
# '&simpleFilter=pool.type:equals:UEXA' if kwargs.get('uk_tote_exacta', False) else ''
# '&simpleFilter=pool.type:equals:UTRI' if kwargs.get('uk_tote_trifecta', False) else ''
# '&simpleFilter=pool.type:equals:UQDP' if kwargs.get('uk_tote_quadpot', False) else ''
# '&simpleFilter=pool.type:equals:UPLP' if kwargs.get('uk_tote_placepot', False) else ''
# '&simpleFilter=pool.type:equals:UJKP' if kwargs.get('uk_tote_jackpot', False) else ''

query = query_builder()\
    .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.EQUALS, 'UEXA'))
s.ss_pool_for_event(event_id=8677919)