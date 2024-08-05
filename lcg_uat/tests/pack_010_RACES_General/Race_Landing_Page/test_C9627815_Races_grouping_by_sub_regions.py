import re
import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, exists_filter, SiteServeRequests, prune
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from crlat_siteserve_client.utils.date_time import get_date_time_as_string


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C9627815_Races_grouping_by_sub_regions(BaseRacing):
    """
    TR_ID: C9627815
    NAME: <Races>: grouping by sub regions
    DESCRIPTION: This test case verifies displaying of <Race> events grouped by sub region
    PRECONDITIONS: 1) To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: 2) TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 3) You should have <Race> events from different types and types should be assigned to different sub regions
    PRECONDITIONS: 4) **Check boxes in 'Flags' section in TI on type level:**
    PRECONDITIONS: - Is in UK - typeFlagCodes="UK"
    PRECONDITIONS: - Is Irish - typeFlagCodes="IE"
    PRECONDITIONS: - South Africa - typeFlagCodes="ZA"
    PRECONDITIONS: - UAE - typeFlagCodes="AE"
    PRECONDITIONS: - Chile - typeFlagCodes="CL"
    PRECONDITIONS: - India - typeFlagCodes="IN"
    PRECONDITIONS: - Australia - typeFlagCodes="AU"
    PRECONDITIONS: - US - typeFlagCodes="US"
    PRECONDITIONS: - France - typeFlagCodes="FR"
    PRECONDITIONS: - Is International - typeFlagCodes="INT"
    PRECONDITIONS: - Virtual Racing - typeFlagCodes="VR"
    PRECONDITIONS: 5) You should be on <Race> landing page
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    end_date = f'{get_date_time_as_string(days=0)}T23:59:59.999Z'
    start_date = f'{get_date_time_as_string(days=-1)}T23:59:59.999Z'
    start_date_minus = f'{get_date_time_as_string(days=-1)}T23:59:59.999Z'

    @staticmethod
    def sort_events_by_type(response):
        events_from_response = {'UK': [], 'IE': [], 'FR': [], 'IN': [], 'AE': [], 'CL': [], 'AU': [], 'US': [],
                                'ZA': [], 'INT': [], 'VR': []}
        events_with_outcomes = []
        for event in response:
            if event['event'].get('children'):
                markets = event['event'].get('children')
                for market in markets:
                    if market.get('market').get('children'):
                        events_with_outcomes.append(event)

        all_events = []
        for event in events_with_outcomes:
            if event['event'].get('typeFlagCodes'):
                flag_codes = event['event'].get('typeFlagCodes').split(',')[:-1]
                for flag in flag_codes:
                    if flag in events_from_response.keys():
                        if event['event']['typeName'] not in all_events:
                            events_from_response[flag].append(event['event']['typeName'])
                            all_events.append(event['event']['typeName'])
                        break

        events_from_response['UK,IE'] = events_from_response['UK']
        events_from_response['UK,IE'].extend(events_from_response['IE'])

        return events_from_response

    def base_filter(self):
        return self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS,
                                      self.ob_config.backend.ti.horse_racing.category_id)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '227')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.NAME, OPERATORS.NOT_EQUALS, '%7Cnull%7C')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                                  OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP'))) \
            .add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_CONTAINS, 'EVFLAG_AP'))

    def get_events(self):
        query_params = self.base_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.NOT_INTERSECTS, 'SP'))
        events = self.ss_req_hr.ss_event_to_outcome_for_class(query_builder=query_params)

        return events

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing event in TI
        """
        self.__class__.ss_req_hr = SiteServeRequests(env=tests.settings.backend_env,
                                                     class_id=self.horse_racing_live_class_ids,
                                                     category_id=self.ob_config.backend.ti.horse_racing.category_id,
                                                     brand=self.brand)
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_international_racing_event(number_of_runners=1, market_extra_place_race=True)
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=True)
            self.__class__.eventID = event_params.event_id
            self.__class__.event_ss_name = 'Autotest - UK'
        else:
            query_params = self.basic_active_events_filter() \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS,
                                          self.ob_config.backend.ti.horse_racing.category_id)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_RESULTED, OPERATORS.IS_FALSE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '227')) \
                .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME, OPERATORS.EQUALS,
                                          self.ob_config.horseracing_config.default_market_name)) \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                                      OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP')))
            events = self.ss_req_hr.ss_event_to_outcome_for_class(query_builder=query_params)
            event = next((event for event in events if
                          event.get('event') and event['event'] and event['event'].get('children')), None)
            self.__class__.eventID = event.get('event').get('id')
            self.__class__.event_ss_name = event['event']['typeName']
            self._logger.info(f'*** Found Horse racing event with id "{self.eventID}"')

        query2 = self.ss_query_builder. \
            add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')). \
            add_filter(exists_filter(LEVELS.EVENT,
                                     simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                   OPERATORS.INTERSECTS, 'MKTFLAG_EPR'))). \
            add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME, OPERATORS.EQUALS,
                                     self.ob_config.horseracing_config.default_market_name)). \
            add_filter(prune(LEVELS.EVENT)). \
            add_filter(prune(LEVELS.MARKET))
        self.__class__.extra_place = self.ss_req_hr.ss_event_to_outcome_for_class(query_builder=query2)

    def test_001_verify_displaying_of_events_by_sub_regions(self):
        """
        DESCRIPTION: Verify displaying of events by sub regions
        EXPECTED: Events are grouped and displayed under respective sub regions sections according to the types configurations:
        EXPECTED: - Is in UK (typeFlagCodes="UK") - displayed within 'UK & IRE' section
        EXPECTED: - Is Irish (typeFlagCodes="IE") - displayed within 'UK & IRE' section
        EXPECTED: - Virtual Racing (typeFlagCode="VR") - displayed within 'Ladbrokes/Coral Legends' section
        EXPECTED: - South Africa (typeFlagCodes="ZA") - displayed within 'South Africa' section
        EXPECTED: - UAE (typeFlagCodes="AE") - displayed within 'UAE' section
        EXPECTED: - Chile (typeFlagCodes="CL") - displayed within 'Chile' section
        EXPECTED: - India (typeFlagCodes="IN") - displayed within 'India' section
        EXPECTED: - Australia (typeFlagCodes="AU") - displayed within 'Austria' section
        EXPECTED: - US (typeFlagCodes="US") - displayed within 'USA' section
        EXPECTED: - France (typeFlagCodes="FR") - displayed within 'France' section
        EXPECTED: - Is International (typeFlagCodes="INT") - displayed within 'Other International' section
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')
        self.__class__.type_flag_codes_flipped = dict((y, x) for x, y in self.type_flag_codes.items())
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.assertTrue(self.site.racing_event_details.meeting_selector.is_displayed(),
                        msg='Meeting Selector is not displayed')

        self.site.racing_event_details.meeting_selector.click()
        self.assertTrue(self.site.racing_event_details.meetings_list.is_displayed(), msg='Meetings list is not shown')

        sections = self.site.racing_event_details.meetings_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        meetings = self.sort_events_by_type(self.get_events())  # Grouped by sub regions (key_flag)

        if self.device_type != 'desktop':
            if self.extra_place:
                next_races = self.site.racing_event_details.meetings_list.next_races_name
                self.assertEqual(next_races, vec.racing.NEXT_RACES.upper(),
                                 msg=f'Incorrect next races tab name.\nActual: "{next_races}" \nExpected: '
                                     f'"{vec.racing.NEXT_RACES.upper()}"')

                offers_and_featured_races = self.site.racing_event_details.meetings_list.offers_and_featured_name
                self.assertEqual(offers_and_featured_races, vec.racing.FEATURED_OFFERS_SECTION_TITLE,
                                 msg=f'Incorrect offers and featured races tab name.\nActual: "{offers_and_featured_races}" \nExpected: '
                                     f'"{vec.racing.FEATURED_OFFERS_SECTION_TITLE}"')

        for section_name, section in list(sections.items()):
            if section_name == 'VIRTUAL RACING':
                section_name = vec.racing.LEGENDS_TYPE_NAME.upper()
            section_name = next((section_nam for section_nam in self.type_flag_codes_flipped.keys() if
                                 section_nam.upper() == section_name.upper()), None)
            section.expand()
            key_flag = self.type_flag_codes_flipped[section_name]
            striped_meeting = []
            ss_meetings = []
            for event in meetings.get(key_flag):
                striped_meeting.append(re.sub(r'\(.*?\)', '', event).strip().upper())
            ss_meetings += striped_meeting
            ui_meetings = section.items_as_ordered_dict.keys()
            if not ui_meetings:
                section.expand()
                ui_meetings = section.items_as_ordered_dict.keys()
            ui_meetings = [re.sub(r'\(.*?\)', '', meeting).strip().upper() for meeting in ui_meetings]
            self.assertListEqual(sorted(ss_meetings), sorted(ui_meetings),
                                 msg=f'Event list got from SS {sorted(ss_meetings)} '
                                     f'is not the same as on UI {sorted(ui_meetings)} for "{section_name}" section')

            # events will show same as mobile as per new update story OZONE-5872--GRAY HOUNDS and OZONE-3480 horse racing
            # else:
            #     del meetings['UK']
            #     del meetings['IE']  # To avoid duplication
            #     ss_meetings = []
            #     for meeting in meetings.values():
            #         striped_meeting = []
            #         for event in meeting:
            #             striped_meeting.append(event.strip())
            #         ss_meetings += striped_meeting
            #     ui_meetings = list(sections.keys())
            #     check = all(item in ss_meetings for item in ui_meetings)
            #     self.assertTrue(check, msg=f'Incorrect list of available meetings.\n'
            #                                f'UI: "{ui_meetings}"\nSS: "{ss_meetings}"')
