from crlat_siteserve_client.constants import *
from crlat_siteserve_client.siteserve_client import query_builder, simple_filter, exists_filter, translation_lang
from tests import s

#Coupon?'
 # 'existsFilter=coupon:simpleFilter:event.startTime:greaterThanOrEqual:{get_yesterday_date}T21:00:00.000Z' \
 # '&existsFilter=coupon:simpleFilter:event.suspendAtTime:greaterThan:{get_today_date}.00Z' \
 # '&existsFilter=coupon:simpleFilter:event.isStarted:isFalse' \ +
 # '&simpleFilter=coupon.siteChannels:contains:M' \ +
 # '&existsFilter=coupon:simpleFilter:event.categoryId:intersects:{category_id}' \
 # '&translationLang=en' \ +
query_builder()\
    .add_filter(simple_filter(LEVELS.COUPON, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M'))\
    .add_filter(exists_filter(LEVELS.COUPON, simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)))\
    .add_filter(exists_filter(LEVELS.COUPON, simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, '16')))\
    .add_filter(translation_lang())
s.ss_coupon(query_builder=query_builder)
