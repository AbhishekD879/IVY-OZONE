import collections
import re
from collections import OrderedDict
from datetime import datetime

import pytest
from crlat_ob_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from deepdiff import DeepDiff

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.featured
@pytest.mark.racing
@pytest.mark.module_ribbon
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.high
@vtest
class Test_C29415_Verify_Race_events_carousel_Race_Time_and_Meeting(BaseRacing, BaseFeaturedTest):
    """
    TR_ID: C29415
    NAME:  Verify <Race> events carousel Race Time & Meeting
    DESCRIPTION: This test case if for checking correctness of <Race> events carousel race time and meeting
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'name'** to check an event name and local time
    PRECONDITIONS: - **'typeName'** to check a race meeting name
    PRECONDITIONS: - **isEachWayAvailable, eachWayFactorDen, ​eachWayPlaces, ​eachWayFactorNum **to check if there are each way terms
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 4) Invictus application is loaded
    """
    keep_browser_open = True
    featured_module_name = None
    section = None
    max_number_of_events = 2
    events_from_hours_delta = -4
    ui_module_events_info = OrderedDict()

    def test_000_preconditions(self):
        """
        DESCRIPTION: In CMS create Featured module created by <Race> type ID
        EXPECTED: Module is created
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]
            search = re.search(r'(?:\d{2}:\d{2})(?:\s\+\d{1,2}d)?\s([\w\s\']+)',
                               event['event']['name'])  # Shepp' Dogs or +1d Fonner Park for example
            race_meting = search.groups()[0]
            self.__class__.race_type_id = event['event']['typeId']
        else:
            self.ob_config.add_UK_racing_event(number_of_runners=2)
            race_meting = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.name_pattern
            self.__class__.race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        self.__class__.featured_module_name = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', id=self.race_type_id, module_time_from_hours_delta=self.events_from_hours_delta,
            events_time_from_hours_delta=self.events_from_hours_delta, max_rows=self.max_number_of_events)['title'].upper()

        self.__class__.is_executed_on_desktop = self.device_type in ['desktop']
        self.__class__.name_pattern = race_meting.upper() if self.brand == 'ladbrokes' else race_meting

        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.featured_module_name)

    def test_001_go_to_module_selector_ribbon_module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID
        EXPECTED: 'Feature' tab is selected by default
        EXPECTED: Module created by <Race> type ID is shown
        """
        if not self.is_executed_on_desktop:
            featured_module = \
                self.site.home.get_module_content(self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

            self.__class__.section = \
                featured_module.accordions_list.items_as_ordered_dict.get(self.featured_module_name)
            self.assertTrue(self.section, msg=f'Section "{self.featured_module_name}" is not found on FEATURED tab')

    def test_002_scroll_the_page_down_to_featured_section_module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section ->-> Module created by <Race> type ID
        EXPECTED: 'Featured' section is displayed below the following sections: Enhanced / Sports offer carousel, In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: Module created by <Race> type ID is shown
        """
        if self.is_executed_on_desktop:
            featured_module = self.site.home.desktop_modules.featured_module
            self.assertTrue(featured_module, msg='"Featured" module is not displayed')

            featured_content = featured_module.tab_content
            featured_modules = featured_content.accordions_list.items_as_ordered_dict.keys()
            self.assertTrue(featured_content.accordions_list, msg='"Featured" module does not contain any accordions')
            self.assertIn(self.featured_module_name, featured_content.accordions_list.items_as_ordered_dict.keys(),
                          msg=f'Module "{self.featured_module_name}" is not displayed. '
                          f'Please check list of all displayed modules:\n"{featured_modules}"')

            self.__class__.section = featured_content.accordions_list.items_as_ordered_dict[self.featured_module_name]
            self.assertTrue(self.section, msg='No accordions displayed in "Featured" section on Home page')

    def test_003_verify_event_section_header_of_race_events_carousel(self):
        """
        DESCRIPTION: Verify event section header of <Race> events carousel
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: Race event section header is shown in the following format:
        EXPECTED: * 'HH:MM EventName'
        EXPECTED: * E/W: x/y odds - places z,j,k
        EXPECTED: Example: "3:25 York E/W: 1/4 odds - places 1,2"
        EXPECTED: Text IS NOT clickable
        EXPECTED: **For Desktop:**
        EXPECTED: Race event section header is shown in the following format: 'HH:MM EventName'
        """
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found')

        for event_name, event in events.items():
            event.scroll_to()
            self.assertRegex(event_name, r'\d{2}:\d{2} %s' % self.name_pattern,
                             msg=f'Event name: "{event_name}" doesn\'t match expected pattern: {self.name_pattern} '
                                 f'(<HH:MM EventName>)')

            each_way_terms_text = event.each_way_terms.text.replace('\n', ' ')
            self.assertRegex(each_way_terms_text, vec.regex.EXPECTED_EACH_WAY_FORMAT_FEATURED,
                             msg=f'Event each way terms: "{each_way_terms_text}" '
                                 f'doesn\'t match expected pattern: {vec.regex.EXPECTED_EACH_WAY_FORMAT_FEATURED}')
            event.each_way_terms.click()
            self.assertTrue(event.is_displayed(),
                            msg=f'Event: "{event_name}" is not displayed after click on each way terms')

            self.__class__.ui_module_events_info[event_name] = each_way_terms_text

    def test_004_verify_each_way_terms_in_event_section_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Verify each way terms in event section header
        EXPECTED: Each way terms are shown if **isEachWayAvailable='true'**
        EXPECTED: EachWay terms are formed from the following attributes:
        EXPECTED: ***" E/W x/y odds - places z,j,k"***
        EXPECTED: where:
        EXPECTED: x = eachWayFactorNum
        EXPECTED: y= eachWayFactorDen
        EXPECTED: z,j,k = eachWayPlaces
        """
        date_time_from = get_date_time_as_string(date_time_obj=datetime.now(),
                                                 time_format='%Y-%m-%dT%H:%M',
                                                 hours=self.events_from_hours_delta)
        self.__class__.start_date = f'{date_time_from}:00.000Z'
        query = self.basic_active_events_filter()
        query.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')).\
            add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.EQUALS, 'true'))
        ss_events_info = self.ss_req.ss_event_to_outcome_for_type(type_id=self.race_type_id, query_builder=query)
        ss_module_events_info = {}

        for ss_event_info in ss_events_info:
            event = ss_event_info['event']
            if not event.get('children'):
                continue
            event_name = event['name']
            market_info = next((market.get('market') for market in event.get('children')), None)
            if not market_info:
                continue
            each_way_factor_num = market_info['eachWayFactorNum']
            each_way_factor_den = market_info['eachWayFactorDen']
            each_way_places = int(market_info['eachWayPlaces'])
            joiner = '-' if self.brand != 'ladbrokes' else ','
            each_way_places_str = joiner.join([str(each_way_place) for each_way_place in range(1, each_way_places + 1)])
            ew_terms_text = vec.sb.ODDS_A_PLACES.format(num=each_way_factor_num,
                                                        den=each_way_factor_den,
                                                        arr=each_way_places_str)
            ss_module_events_info[event_name] = ew_terms_text

        # Need to get sorted list of displayed events as they got from SiteServe in random order
        self.__class__.ss_module_events_info_all = collections.OrderedDict(list(sorted(ss_module_events_info.items())))
        if not self.is_executed_on_desktop:
            actual_list = list(self.ui_module_events_info.values())
            expected_list = list(self.ss_module_events_info_all.values())[:self.max_number_of_events]
            result = DeepDiff(actual_list, expected_list, ignore_order=True)
            self.assertFalse(bool(result), msg=f'\nActual module: "{self.featured_module_name}" '
                                               f'displayed EachWay terms:\n{actual_list},'
                                               f'\nexpected got from SiteServe:\n{expected_list}')

    def test_005_verify_race_meeting_correctness(self):
        """
        DESCRIPTION: Verify race meeting correctness
        EXPECTED: Race Meeting name corresponds to the SiteServer response.
        EXPECTED: From the list of events look at the attribute **'typeName'** near the selected event
        EXPECTED: Event time corresponds to the race local time (see** 'name' **attribute from the Site Server response)
        """
        actual_list = set(map(lambda x: x.upper(), self.ui_module_events_info.keys()))
        expected_list = set(map(lambda x: x.upper(), self.ss_module_events_info_all.keys()))
        self.assertTrue(actual_list.issubset(expected_list),
                        msg=f'\nActual module: "{self.featured_module_name}" '
                            f'displayed events:\n{actual_list},'
                            f'\nexpected got from SiteServe:\n{expected_list}')
