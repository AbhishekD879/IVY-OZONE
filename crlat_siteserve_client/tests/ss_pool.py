from crlat_siteserve_client.constants import *
from crlat_siteserve_client.siteserve_client import query_builder, simple_filter, translation_lang
from tests import s


# Pool
# ?simpleFilter=pool.type:equals:V15' \
# '&simpleFilter=pool.isActive
# &translationLang=en'
query = query_builder()\
    .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.EQUALS, 'V15'))\
    .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.IS_ACTIVE))\
    .add_filter(translation_lang())
s.ss_pool(query_builder=query)
