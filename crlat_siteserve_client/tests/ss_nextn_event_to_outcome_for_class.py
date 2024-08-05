from crlat_siteserve_client.constants import *
from crlat_siteserve_client.siteserve_client import query_builder, simple_filter, exists_filter, price_history, \
    limit_records
from tests import s


# NextNEventToOutcomeForClass
#'?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT' \
 # '&simpleFilter=event.isActive:isTrue' \
 # '&existsFilter=event:simpleFilter:market.name:equals:%7CWin%20or%20Each%20Way%7C' \
 # '&simpleFilter=market.name:equals:%7CWin%20or%20Each%20Way%7C' \
 # '&priceHistory=true' \
 # '&simpleFilter=outcome.name:notEquals:UNNAMED%20FAVOURITE' \
 # '&simpleFilter=outcome.name:notEquals:%7CUNNAMED%20FAVOURITE%7C' \
 # '&simpleFilter=outcome.name:notEquals:UNNAMED%202nd%20FAVOURITE' \
 # '&simpleFilter=outcome.name:notEquals:%7CUNNAMED%202nd%20FAVOURITE%7C' \
 # '&racingForm=outcome' \
 # '&limitRecords=outcome:5' \
 # '&simpleFilter=event.siteChannels:contains:M' \
 # '&simpleFilter=outcome.outcomeStatusCode:equals:A' \
 # '&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A' \
 # '&simpleFilter=market.marketStatusCode:equals:A' \
 # '&simpleFilter=event.eventStatusCode:equals:A' \

query = query_builder()\
 .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'UK,IE,INT'))\
 .add_filter(exists_filter(LEVELS.EVENT, filter_builder=simple_filter(LEVELS.MARKET, ATTRIBUTES.NAME, OPERATORS.EQUALS, '%7CWin%20or%20Each%20Way%7C')))\
 .add_filter(price_history(value='true'))\
.add_filter(limit_records(LEVELS.OUTCOME, '5'))
s.ss_next_n_event_to_outcome_for_class(class_id='227', n=5, query_builder=query)





