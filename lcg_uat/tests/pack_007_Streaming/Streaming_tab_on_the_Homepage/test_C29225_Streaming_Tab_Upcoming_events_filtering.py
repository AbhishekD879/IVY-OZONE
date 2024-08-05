import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
import voltron.environments.constants as vec
from tests.Common import Common
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't be executed, can't create OB event on prod
# @pytest.mark.hl
@pytest.mark.outrights
@pytest.mark.module_ribbon
@pytest.mark.desktop
@pytest.mark.streaming
@pytest.mark.medium
@vtest
class Test_C29225_Streaming_Tab_Upcoming_events_filtering(Common):
    """
    TR_ID: C29225
    NAME: Streaming Tab Upcoming events filtering
    PRECONDITIONS: To get information about event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/xxxx?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   x.xx latest supported SiteServer version
    PRECONDITIONS: *   xxxx event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    today_format_pattern = '%Y-%m-%dT%H:%M:%S.000Z'

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

    def verify_start_time_is_today(self, event):
        todays_date = self.start_date
        todays_date_converted = self.convert_time_to_local(ob_format_pattern=self.today_format_pattern,
                                                           date_time_str=todays_date, ss_data=True).split()[-1]
        event_start_time = event[ATTRIBUTES.START_TIME]
        event_time_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                          date_time_str=event_start_time, ss_data=True).split()[-1]
        self.assertEqual(todays_date_converted, event_time_converted,
                         msg=f'Event day "{todays_date_converted}" is not the same '
                             f'as got from response "{event_time_converted}"')

    def verify_drilldown_tag_names(self, event):
        self.assertIn(ATTRIBUTES.DRILLDOWN_TAG_NAMES, event.keys(),
                      msg=f'There\'s no property "{ATTRIBUTES.DRILLDOWN_TAG_NAMES}" in SS response. '
                      f'See all available properties: {event.keys()}')
        self.assertIn('EVFLAG_PVM' and 'EVFLAG_BL', event[ATTRIBUTES.DRILLDOWN_TAG_NAMES],
                      msg=f'There\'s no property "EVFLAG_PVM" and "EVFLAG_BL" in SS response. '
                      f'See all available properties: {event[ATTRIBUTES.DRILLDOWN_TAG_NAMES]}')

    def verify_is_market_bet_in_run(self, market):
        self.assertIn(ATTRIBUTES.IS_MARKET_BET_IN_RUN, market.keys(),
                      msg=f'There\'s no property "{ATTRIBUTES.IS_MARKET_BET_IN_RUN}" in SS response. '
                      f'See all available properties: {market.keys()}')
        self.assertEquals(market[ATTRIBUTES.IS_MARKET_BET_IN_RUN], 'true',
                          msg=f'Incorrect value for "{ATTRIBUTES.IS_MARKET_BET_IN_RUN}" in SS response.\nActual: '
                          f'"{market[ATTRIBUTES.IS_MARKET_BET_IN_RUN]}"\nExpected: "true"')

    def verify_is_stated(self, event):
        self.assertIn(ATTRIBUTES.IS_STARTED, event.keys(),
                      msg=f'There\'s  property "{ATTRIBUTES.RAW_IS_OFF_CODE}" in SS response.')
        self.assertNotEquals(event[ATTRIBUTES.RAW_IS_OFF_CODE], 'true',
                             msg=f'Incorrect value for "{ATTRIBUTES.RAW_IS_OFF_CODE}" in SS response.\nActual: '
                             f'"{event[ATTRIBUTES.RAW_IS_OFF_CODE]}"\nExpected: not "true"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create 2 events with and without outrights
        """
        self.__class__.outright_event = self.ob_config.add_autotest_premier_league_football_outright_event(is_upcoming=True, perform_stream=True)
        self.__class__.eventID = self.outright_event.event_id
        self.ob_config.change_is_off_flag(self.eventID, is_off=True)

        self.__class__.event_params = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, perform_stream=True)
        self.__class__.event_id = self.event_params.event_id
        self.ob_config.change_is_off_flag(self.event_id, is_off=True)
        self.__class__.expected_active_btn = vec.inplay.LIVE_NOW_SWITCHER

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED:
        """
        self.site.wait_content_state('HomePage')

    def test_002_select_live_stream_tab_from_module_selector_ribbon(self):
        """
        DESCRIPTION: Select 'Live Stream' tab from Module Selector Ribbon
        EXPECTED: *   'Live Stream' tab is opened
        EXPECTED: *   'Live Now' sorting type is selected by default
        """
        name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream)

        if self.device_type == 'desktop':
            cms_right_menu_items = self.cms_config.get_left_menu_items()
            if name in cms_right_menu_items:
                self.site.open_sport(name=name)
            else:
                self.navigate_to_page(name='live-stream')
            self.site.wait_content_state(state_name='LiveStream')
            self.site.wait_content_state('LiveStream')

            active_tab = self.site.live_stream.tabs_menu.current
            self.assertEqual(active_tab, self.expected_active_btn,
                             msg=f'"{active_tab}" sorting type is not selected by default "{self.expected_active_btn}"')
        else:
            self.site.home.get_module_content(module_name=name)
            self.assertTrue(self.site.home.tab_content.has_live_now_section,
                            msg=f'No "{vec.inplay.LIVE_NOW_EVENTS_SECTION}" section is found on Live Stream tab')
            self.assertTrue(self.site.home.tab_content.has_upcoming_section,
                            msg=f'No "{vec.inplay.UPCOMING_EVENTS_SECTION}" section is found on Live Stream tab')

    def test_003_tap_upcoming_sorting_type_button(self):
        """
        DESCRIPTION: Tap 'Upcoming' sorting type button
        """
        if self.device_type == 'desktop':
            self.site.live_stream.tabs_menu.items_as_ordered_dict[vec.inplay.UPCOMING_SWITCHER].click()

    def test_004_verify_events_that_are_present(self):
        """
        DESCRIPTION: Verify events that are present
        EXPECTED: Events which satisfy the following conditions should be present on the page:
        EXPECTED: **NOT Outrights:**
        EXPECTED: *   **drilldownTagNames **should include the following attributes: {EVFLAG_BL and EVFLAG_IVM} OR {EVFLAG_BL, EVFLAG_PVM} OR {EVFLAG_BL, EVFLAG_IVM, EVFLAG_PVM}(on the Event level)** **
        EXPECTED: *   AND **isMarketBetInRun="true" **(on the any Market level)
        EXPECTED: *   **event **startTime **is today**
        EXPECTED: **Outrights:**
        EXPECTED: *   **eventSortCode="TNMT"**
        EXPECTED: *   **drilldownTagNames **should include the following attributes: {EVFLAG_BL and EVFLAG_IVM} OR {EVFLAG_BL, EVFLAG_PVM} OR {EVFLAG_BL, EVFLAG_IVM, EVFLAG_PVM}(on the Event level)** **
        EXPECTED: *   AND **isMarketBetInRun="true" **(on the any Market level)
        EXPECTED: *   **event **startTime **is today**
        EXPECTED: Events should NOT have:
        EXPECTED: *   isStarted=true OR rawIsOffCode=Y
        """
        outright_event, outright_market = self.get_event_and_market_from_ss(self.eventID)
        event, market = self.get_event_and_market_from_ss(self.event_id)

        self.verify_drilldown_tag_names(event)
        self.verify_is_market_bet_in_run(market)
        self.verify_start_time_is_today(event)

        self.verify_drilldown_tag_names(outright_event)
        self.verify_is_market_bet_in_run(outright_market)
        self.verify_start_time_is_today(outright_event)

        self.verify_is_stated(event)
        self.verify_is_stated(outright_event)
