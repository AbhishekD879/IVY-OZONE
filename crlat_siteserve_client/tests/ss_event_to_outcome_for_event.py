from crlat_siteserve_client.constants import *
from crlat_siteserve_client.siteserve_client import query_builder, simple_filter, exists_filter, translation_lang, \
    prune, external_keys, racing_form
from tests import s



# EventToOutcomeForEvent
# filters += '&racingForm=outcome&racingForm=event' if is_racing_form else filters
# params = 'openbet-ssviewer/Drilldown/{version}/EventToOutcomeForEvent/{event_id}?externalKeys=event{filters}'
form_query = query_builder()\
.add_filter(external_keys(level=LEVELS.EVENT))\
.add_filter(racing_form(level=LEVELS.EVENT))\
.add_filter(racing_form(level=LEVELS.OUTCOME))
s.ss_event_to_outcome_for_event(event_id=8677919, query_builder=form_query)
