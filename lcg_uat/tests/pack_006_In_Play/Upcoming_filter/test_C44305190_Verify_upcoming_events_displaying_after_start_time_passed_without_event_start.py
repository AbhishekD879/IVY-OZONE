import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.helpers import get_inplay_event_initial_data


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.in_play
@vtest
class Test_C44305190_Verify_upcoming_events_displaying_after_start_time_passed_without_event_start(Common):
    """
    TR_ID: C44305190
    NAME: Verify upcoming events displaying after start time passed without event start
    DESCRIPTION: This test case verifies upcoming events displaying after start time passed without event start
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Make sure that Upcoming events are present in 'Upcoming' section of 'In-Play' page (for mobile/tablet) or when 'Upcoming' switcher is selected (for Desktop)
    PRECONDITIONS: 3. Make sure there is the event with the following settings:
    PRECONDITIONS: * startTime of less than or equal current time in UTC plus 24 hours
    PRECONDITIONS: * 'drilldownTagNames' with 'EVFLAG_BL'
    PRECONDITIONS: * at least one market with attribute 'isMarketBetInRun' = 'true'
    PRECONDITIONS: * WITHOUT attribute is_off='Y' and without attribute 'isStarted'
    PRECONDITIONS: Note:
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::UPCOMING_EVENT::XXX"
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    """
    keep_browser_open = True
    enable_bs_performance_log = True

    def verify_event_filtering(self):
        events = get_inplay_event_initial_data(category_id=str(self.ob_config.football_config.category_id))
        for event in events:
            if event['name'] == self.event_name:
                self.assertEqual('A', event['eventStatusCode'],
                                 msg='Event attribute siteChannels does not contain "M".')
                self.assertEqual(False, event['eventIsLive'],
                                 msg='Event attribute siteChannels does not contain "M".')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        start_time_upcoming = self.get_date_time_formatted_string(hours=10)
        event = self.ob_config.add_tennis_event_to_autotest_trophy(start_time=start_time_upcoming, is_upcoming=True)
        self.__class__.event_id = event.event_id
        self.__class__.event_name = event.ss_response['event']['name']
        if self.device_type == 'desktop':
            self.__class__.section_name = f"{event.ss_response['event']['categoryCode']} - {event.ss_response['event']['typeName']}"
        else:
            self.__class__.section_name = f"{event.ss_response['event']['typeName']}"

    def test_001_verify_upcoming_events_within_the_page(self):
        """
        DESCRIPTION: Verify upcoming events within the page
        EXPECTED: Event from the preconditions is present within the 'Upcoming' section
        """
        self.navigate_to_page('/in-play/tennis')
        self.site.wait_content_state_changed(timeout=30)
        if self.device_type in ['mobile', 'tablet']:
            switcher_tabs = self.site.inplay.tab_content.items_as_ordered_dict
            upcoming_tab = switcher_tabs[vec.inplay.UPCOMING_EVENTS_SECTION]
            self.assertTrue(upcoming_tab, msg='"In-play" tab contents are not available ')
        else:
            switcher_tabs = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict
            upcoming_tab = switcher_tabs[vec.inplay.UPCOMING_SWITCHER]
            upcoming_tab.click()

    def test_002_verify_event_attributes(self):
        """
        DESCRIPTION: Verify event attributes
        EXPECTED: Upcoming events do not include attributes:
        EXPECTED: * 'isNext24HourEvent'
        EXPECTED: Upcoming events include attributes:
        EXPECTED: * eventStatusCode: "A"
        EXPECTED: * isLiveNowOrFutureEvent: "true"
        """
        self.verify_event_filtering()

    def test_003_modify_event_to_be_defined_by_attributes_is_off__y_and_event_attribute_isstarted(self):
        """
        DESCRIPTION: Modify event to be defined by attributes is_off = 'Y' and event attribute isStarted
        EXPECTED: * Event disappears from 'Upcoming' section
        EXPECTED: * Event is displayed in 'In-Play' section
        """
        self.ob_config.change_is_off_flag(event_id=self.event_id, is_off=True)
        sleep(5)
        self.navigate_to_page('/in-play/tennis')
        self.site.wait_content_state_changed(timeout=30)
        if self.device_type in ['mobile', 'tablet']:
            switcher_tabs = self.site.inplay.tab_content.items_as_ordered_dict
            live_now = switcher_tabs[vec.inplay.LIVE_NOW_EVENTS_SECTION]
            self.assertTrue(live_now, msg='"In-play" tab contents are not available ')
        else:
            switcher_tabs = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict
            live_now = switcher_tabs[vec.inplay.LIVE_NOW_SWITCHER]
            live_now.click()
        sleep(2)
        leagues = self.site.inplay.tab_content.accordions_list
        league = leagues.items_as_ordered_dict
        self.assertTrue(league, msg='No Live now events are available')
        events = league[self.section_name.upper()]
        event = events.items_as_ordered_dict
        self.assertIn(self.event_name, event.keys(), msg=f'Expected event is not appearing on live now section')
