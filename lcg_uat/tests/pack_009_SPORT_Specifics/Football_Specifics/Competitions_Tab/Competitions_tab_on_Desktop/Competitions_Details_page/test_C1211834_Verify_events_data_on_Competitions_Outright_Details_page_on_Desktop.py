import pytest
import tests
import time
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C1211834_Verify_events_data_on_Competitions_Outright_Details_page_on_Desktop(BaseSportTest):
    """
    TR_ID: C1211834
    NAME: Verify events data on Competitions Outright Details page on Desktop
    DESCRIPTION: This test case verifies events data on Competitions Outright Details page on Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: * XXX - the event ID
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    outright_name = 'Outright %s' % int(time.time())

    def get_event_and_market_from_ss(self, event_id: str) -> tuple:
        """
        Gets event and market for given event from SS response
        :param event_id: specifies event id
        :return: tuple with event and market attributes and their values
        """
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        events = resp[0]['event']
        markets = resp[0]['event']['children'] if 'event' in resp[0] and 'children' in resp[0]['event'] else []
        return events, markets[0]['market']

    def verify_drilldown_tag_names(self, event):
        self.assertIn(ATTRIBUTES.DRILLDOWN_TAG_NAMES, event.keys(),
                      msg=f'There\'s no property "{ATTRIBUTES.DRILLDOWN_TAG_NAMES}" in SS response. '
                      f'See all available properties: {event.keys()}')
        self.assertIn('EVFLAG_PVM' and 'EVFLAG_BL', event[ATTRIBUTES.DRILLDOWN_TAG_NAMES],
                      msg=f'There\'s no property "EVFLAG_PVM" and "EVFLAG_BL" in SS response. '
                      f'See all available properties: {event[ATTRIBUTES.DRILLDOWN_TAG_NAMES]}')

    def verify_raw_is_off_code(self, event):
        self.assertIn(ATTRIBUTES.RAW_IS_OFF_CODE, event.keys(),
                      msg=f'There\'s no property "{ATTRIBUTES.RAW_IS_OFF_CODE}" in SS response. '
                      f'See all available properties: {event.keys()}')
        self.assertEquals(event[ATTRIBUTES.RAW_IS_OFF_CODE], 'Y',
                          msg=f'Incorrect value for "{ATTRIBUTES.RAW_IS_OFF_CODE}" in SS response.\nActual: '
                          f'"{event[ATTRIBUTES.RAW_IS_OFF_CODE]}"\nExpected: "Y"')

    def verify_is_market_bet_in_run(self, market):
        self.assertIn(ATTRIBUTES.IS_MARKET_BET_IN_RUN, market.keys(),
                      msg=f'There\'s no property "{ATTRIBUTES.IS_MARKET_BET_IN_RUN}" in SS response. '
                      f'See all available properties: {market.keys()}')
        self.assertEquals(market[ATTRIBUTES.IS_MARKET_BET_IN_RUN], 'true',
                          msg=f'Incorrect value for "{ATTRIBUTES.IS_MARKET_BET_IN_RUN}" in SS response.\nActual: '
                          f'"{market[ATTRIBUTES.IS_MARKET_BET_IN_RUN]}"\nExpected: "true"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create 2 events with and without outrights
        """
        league = tests.settings.football_autotest_competition_league
        self.__class__.outright_event = self.ob_config.add_autotest_premier_league_football_outright_event(
            is_live=True, perform_stream=True, event_name=self.outright_name)
        if self.brand == 'ladbrokes':
            self.__class__.league_name = f'{self.get_accordion_name_for_event_from_ss(self.outright_event.ss_response)}'.title()
        else:
            self.__class__.league_name = f'{tests.settings.football_autotest_competition} - {league}'

        self.__class__.eventID = self.outright_event.event_id
        self.ob_config.change_is_off_flag(self.eventID, is_off=True)
        self.__class__.expected_active_btn = vec.inplay.LIVE_NOW_SWITCHER

        self.__class__.event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                                                perform_stream=True)
        self.__class__.event_name = self.event_params.team1 + ' v ' + self.event_params.team2
        self.__class__.event_id = self.event_params.event_id
        self.ob_config.change_is_off_flag(self.event_id, is_off=True)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='Football')

    def test_002_navigate_to_football_competitions_details_page(self):
        """
        DESCRIPTION: Navigate to Football Competitions Details page
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' and 'Outrights' switchers are displayed in the same row as 'Market Selector' below the Competitions header and Breadcrumbs trail
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        """
        expected_sport_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                    self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')

    def test_003_choose_outrights_switcher_and_verify_outright_event_details(self):
        """
        DESCRIPTION: Choose 'Outrights' switcher and verify Outright event details
        EXPECTED: **Pre-match events:**
        EXPECTED: Events with next attributes are shown:
        EXPECTED: *   **eventSortCode="TNMT"**/"TRxx" ****(xx - numbers from 01 to 20)
        EXPECTED: *   AND/OR **dispSortName **is positive (e.g. dispSortName="3W")
        EXPECTED: **Started events:**
        EXPECTED: Events with the following attributes are shown:
        EXPECTED: *   **eventSortCode="TNMT"**/"TRxx" ****(xx - numbers from 01 to 20) AND/OR ​**dispSortName **is positive (e.g. dispSortName="3W")
        EXPECTED: *   AND **isMarketBetInRun="true" **(on the any Market level)
        EXPECTED: *   AND **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
        """
        self.site.football.tabs_menu.click_button('OUTRIGHTS')
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, 'OUTRIGHTS',
                         msg=f'OUTRIGHTS tab is not active, active is "{active_tab}"')
        event, market = self.get_event_and_market_from_ss(self.event_id)
        self.verify_is_market_bet_in_run(market)
        self.verify_drilldown_tag_names(event)
        self.verify_raw_is_off_code(event)

    def test_004_verify_outrights_events_and_markets_attribute(self):
        """
        DESCRIPTION: Verify Outrights events and markets attribute
        EXPECTED: * Event name on 'Event Name Panel' corresponds to '**name**' attribute
        EXPECTED: * Event start date corresponds to '**startTime**' attribute
        EXPECTED: and it is shown in ** '<name of the day>, DD-MMM-YY 24 hours HH:MM'** format (e.g. 14:00 or 05:00)
        EXPECTED: * 'Each Way' terms is shown if '**isEachWayAvailable="true"**' attribute is received on market level
        EXPECTED: * 'LIVE' label is shown if event is live now: **rawIsOffCode="Y"** OR **rawIsOffCode="-"** AND **isStarted="true"**
        """
        # Covered in step 3

    def test_005_verify_events_order_on_competitions_details_page_outrights_switcher_that_has_several_outright_events_ie_world_cup_2018_europa_cup_copa_america_etc(self):
        """
        DESCRIPTION: Verify events order on Competitions Details page ('Outrights' switcher) that has several Outright events (i.e. 'World Cup 2018', 'Europa Cup', 'Copa America' etc.)
        EXPECTED: Events are ordered in the following way:
        EXPECTED: * 'startTime' - chronological order in the first instance
        EXPECTED: * Event 'displayOrder' in ascending
        EXPECTED: * Alphabetical order
        """
        self.test_002_navigate_to_football_competitions_details_page()
        grouping_buttons = self.site.football.tab_content.grouping_buttons
        self.__class__.sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='Sections not found')

        self.assertTrue(grouping_buttons.items_as_ordered_dict, msg='No grouping buttons found')
        if self.brand == 'bma':
            self.assertListEqual(list(grouping_buttons.items_as_ordered_dict.keys()),
                                 [vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME.upper(),
                                  vec.sb_desktop.COMPETITIONS_SPORTS.upper()],
                                 msg=f'Grouping buttons are not the same as expected')
        else:
            self.assertListEqual(list(grouping_buttons.items_as_ordered_dict.keys()),
                                 [vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME,
                                  vec.sb_desktop.COMPETITIONS_SPORTS],
                                 msg=f'Grouping buttons are not the same as expected')

    def test_006_verify_markets_order_on_competitions_details_page(self):
        """
        DESCRIPTION: Verify markets order on Competitions Details page
        EXPECTED: Markets are ordered in the following way:
        EXPECTED: * Market 'displayOrder' in ascending
        EXPECTED: * Depends on ordering received in response from OB
        """
        competition_module_items = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        if not competition_module_items:
            raise SiteServeException('There are no available In-Play events')
