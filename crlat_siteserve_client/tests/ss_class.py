from crlat_siteserve_client.constants import *
from crlat_siteserve_client.siteserve_client import query_builder, simple_filter, exists_filter, translation_lang, \
    prune, external_keys, racing_form
from tests import s

#Class' \
 # '?simpleFilter=class.categoryId:equals:{category_id}' \
 # '&simpleFilter=class.isActive' \
 # '&simpleFilter=class.siteChannels:contains:M' \
 # '&translationLang=en'.format(version=self.version, category_id=category_id)
class_query = query_builder()\
    .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, '1'))\
    .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE))\
    .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M'))\
    .add_filter(translation_lang())
s.ss_class(query_builder=class_query)


