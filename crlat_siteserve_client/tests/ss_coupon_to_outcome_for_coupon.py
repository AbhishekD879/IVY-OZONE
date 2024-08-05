from crlat_siteserve_client.constants import *
from crlat_siteserve_client.siteserve_client import query_builder, simple_filter
from tests import s


#CouponToOutcomeForCoupon
#'?simpleFilter=event.categoryId:intersects:{category_id}' \
# '&simpleFilter=event.siteChannels:contains:M' \
# '&simpleFilter=event.isStarted:isFalse' \

query = query_builder()\
    .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, '1'))\
    .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M'))\
    .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE))
s.ss_coupon_to_outcome_for_coupon(coupon_id='319', query_builder=query)

