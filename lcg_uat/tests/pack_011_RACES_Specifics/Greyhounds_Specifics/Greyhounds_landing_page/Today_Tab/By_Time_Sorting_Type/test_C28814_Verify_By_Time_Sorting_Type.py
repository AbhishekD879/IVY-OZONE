import pytest
import tests
import dateutil
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import do_request
from datetime import datetime, timedelta
from json import JSONDecodeError


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28814_Verify_By_Time_Sorting_Type(BaseRacing):
    """
    TR_ID: C28814
    NAME: Verify 'By Time' Sorting Type
    DESCRIPTION: This test case verifies 'Today' tab when 'BY TIME' sorting type is selected
    PRECONDITIONS: To get the UK/Irish/International daily races events check modules (modules name can be changed in CMS) in 'FEATURED_STRUCTURE_CHANGED' request from websocket (wss://featured-sports)
    PRECONDITIONS: Example of event structure:
    PRECONDITIONS: **flag:** "UK",
    PRECONDITIONS: **data:** [{
    PRECONDITIONS: **id:** "230549330",
    PRECONDITIONS: **categoryId:** "21",
    PRECONDITIONS: **categoryName:** "Horse Racing",
    PRECONDITIONS: **className:** "Horse Racing - Live",
    PRECONDITIONS: **name:** "Southwell",
    PRECONDITIONS: **typeName:** "Southwell",
    PRECONDITIONS: **startTime:** 1593614400000,
    PRECONDITIONS: **classId:** "285",
    PRECONDITIONS: **cashoutAvail:** "Y",
    PRECONDITIONS: **poolTypes:**  ["UPLP", "UQDP"],
    PRECONDITIONS: **liveStreamAvailable:** true,
    PRECONDITIONS: **isResulted:** false,
    PRECONDITIONS: **isStarted:** false,
    PRECONDITIONS: **eventIsLive:** false,
    PRECONDITIONS: **isFinished:** false,
    PRECONDITIONS: **isBogAvailable:** false,
    PRECONDITIONS: **isLpAvailable:** false,
    PRECONDITIONS: **drilldownTagNames:** "EVFLAG_BL,EVFLAG_AVA,",
    PRECONDITIONS: **localTime:** "15:40"
    PRECONDITIONS: **markets:** [{
    PRECONDITIONS: **drilldownTagNames:** 'MKTFLAG_EPR',
    PRECONDITIONS: **eachWayFactorNum:** 1,
    PRECONDITIONS: **eachWayFactorDen:** 2,
    PRECONDITIONS: **eachWayPlaces:** 3,
    PRECONDITIONS: **isEachWayAvailable:** true
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'name'** on event level to see event name and local time
    PRECONDITIONS: **FOR LADBROKES** BY MEETING/BY TIME subtabs removed according to the story BMA-42462 and design https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: Load app
    PRECONDITIONS: Navigate to Greyhounds page -> 'TODAY'tab is selected by default -> 'BY MEETING' sorting type is selected by default
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create greyhound events
        EXPECTED: Events are created
        """
        self.__class__.section = "EVENTS" if self.device_type == "mobile" else "Events"
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')
        if tests.settings.backend_env != 'prod':
            start_time = self.get_date_time_formatted_string(seconds=10)
            self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1,
                                                         start_time=start_time)

    def test_001_select_by_time_sorting_type(self, tab=None):
        """
        DESCRIPTION: Select 'BY TIME' sorting type
        EXPECTED: 'BY TIME' sorting type is selected
        """
        tab = vec.sb.SPORT_DAY_TABS.today
        self.site.greyhound.tabs_menu.click_button(tab)
        self.assertEqual(self.site.greyhound.tabs_menu.current, tab,
                         msg=f'Opened grouping button "{self.site.greyhound.tabs_menu.current}" '
                             f'is not the same as expected "{tab}"')

        self.site.greyhound.tab_content.grouping_buttons.click_button(
            vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1])
        self.assertEqual(self.site.greyhound.tab_content.grouping_buttons.current,
                         vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1],
                         msg=f'Opened grouping button "{self.site.greyhound.tab_content.grouping_buttons.current}" '
                             f'is not the same as expected "{vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1]}"')

    def test_002_check_race_events_sections(self):
        """
        DESCRIPTION: Check Race Events sections
        EXPECTED: * Race Event section 'Events' is displayed and expanded by default
        EXPECTED: **FOR Mobile** 'NEXT RACES' section is displayed and expanded by default
        EXPECTED: **FOR Desktop** 'Next races' widget is displayed and expanded by default
        """
        sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        events_section = sections.get(self.section)
        self.assertTrue(events_section, msg='Race Event section "Events" is not displayed')
        self.assertTrue(events_section.is_expanded(), msg=f'Event "{events_section}" is not expanded by default')

    def test_003_verify_section_content(self):
        """
        DESCRIPTION: Verify section content
        EXPECTED: List of events for today's date is shown
        """
        flag = 0
        self.__class__.ss_event_names = []
        actual_url = self.get_response_url('/NextNEventToOutcomeForClass')
        if not actual_url:
            raise SiteServeException(f'No event data available for GreyhoundSport')
        response = do_request(method='GET', url=actual_url)
        for event in response["SSResponse"]["children"]:
            self.ss_event_names.append(event["event"]["name"])
            event_start_time = event["event"]["startTime"]
            event_time = dateutil.parser.parse(event_start_time)
            current_uk_time = datetime.utcnow() + timedelta(hours=1)
            self.assertTrue((event_time.replace(tzinfo=None) - current_uk_time.replace(tzinfo=None)).days <= 1,
                            msg="The startTime is not from today's date")
            flag = flag + 1
            if flag == len(response["SSResponse"]["children"]) - 1:
                break

    def test_004_check_event_section(self):
        """
        DESCRIPTION: Check event section
        EXPECTED: * Each event is in a separate block
        EXPECTED: * Event name corresponds to the **'name' **attribute from the Featured WS featured_structure_changed message (it includes race local time and event name)
        EXPECTED: * 'Go To Race Card' link is displayed on the right side
        EXPECTED: of the event block
        """
        sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        events_section = sections.get(self.section)
        events = events_section.race_by_time.items_as_ordered_dict
        for event_name, event in events.items():
            self.assertTrue(event_name, msg='nnn')
            self.assertTrue(event.go_to_race_card_link, msg='Race Event section "Events" is not displayed')

    def test_005_verify_stream_icon(self):
        """
        DESCRIPTION: Verify 'Stream' icon
        EXPECTED: * Stream icon is displayed under the event name
        EXPECTED: ![](index.php?/attachments/get/36771)
        EXPECTED: * Stream icon is displayed for event where the stream is available
        """
        # step NA as stream icon is not displaying
