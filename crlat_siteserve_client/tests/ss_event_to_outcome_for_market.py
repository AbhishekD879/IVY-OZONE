from crlat_siteserve_client.constants import *
from crlat_siteserve_client.siteserve_client import query_builder, simple_filter
from tests import s



# EventToOutcomeForMarket
# '?simpleFilter=event.siteChannels:contains:M'

query = query_builder()\
    .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M'))
s.ss_events_to_outcome_for_markets(market_ids=[123432,43546])

