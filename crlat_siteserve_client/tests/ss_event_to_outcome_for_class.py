from crlat_siteserve_client.constants import *
from crlat_siteserve_client.siteserve_client import query_builder, simple_filter, exists_filter, translation_lang, \
    prune
from tests import s


# EventToOutcomeForClass
# &simpleFilter=event.eventStatusCode:equals:A
#'&existsFilter=event:simpleFilter:market.drilldownTagNames:notIntersects:MKTFLAG_SP'
#'&simpleFilter=outcome.outcomeStatusCode:equals:A'
# '&simpleFilter=event.typeName.equals:Newmarket
#&prune=event'
#'&prune=market'

query = query_builder()\
    .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_NAME, OPERATORS.EQUALS, '|Enhanced Multiples|'))\
    .add_filter(prune(LEVELS.EVENT))\
    .add_filter(prune(LEVELS.MARKET))

s.ss_event_to_outcome_for_class(class_id='227', query_builder=query)