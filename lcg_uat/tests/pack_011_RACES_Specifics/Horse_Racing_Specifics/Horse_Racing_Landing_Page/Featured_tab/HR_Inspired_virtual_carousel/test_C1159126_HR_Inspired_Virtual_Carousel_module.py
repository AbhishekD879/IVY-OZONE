import pytest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1159126_HR_Inspired_Virtual_Carousel_module(BaseRacing):
    """
    TR_ID: C1159126
    NAME: HR Inspired Virtual Carousel module
    DESCRIPTION: This test case verifies Carousel module on the Horse Racing Landing page with count down timer for the video
    PRECONDITIONS: - Ordering of HR Inspired Virtual Carousel module is configured in CMS
    PRECONDITIONS: - Video starts on 1min20 sec earlier than event starts (Video starts = eventStartTime + 1min20 sec. )
    PRECONDITIONS: - "eventIsOff" time = 45 seconds after stream for an event is finished.
    PRECONDITIONS: - To get the Inspired Virtual events check modules ('Virtual Race Carousel' module, the name can be changed in CMS) in 'FEATURED_STRUCTURE_CHANGED' request from websocket (wss://featured-sports)
    PRECONDITIONS: Example of Virtual event structure:
    PRECONDITIONS: {
    PRECONDITIONS: id: "230549330",
    PRECONDITIONS: name: "Derby Downs",
    PRECONDITIONS: startTime: "2020-06-19T17:26:00Z",
    PRECONDITIONS: classId: "285"
    PRECONDITIONS: }
    PRECONDITIONS: - Amount of events in Inspired Virtual carousel can be set in CMS: Sports Pages-> Sport Categories -> Horse Racing/Greyhounds -> **'limit'** field
    PRECONDITIONS: Default value is 5, min is 1, max is 12 events.
    PRECONDITIONS: - Types and classes for Inspired Virtuals can be changed in CMS: Sports Pages-> Sport Categories -> Horse Racing/Greyhounds -> **'excludeTypeIDs'** and **'classId'** fields
    PRECONDITIONS: **'excludeTypeIDs' default values for different profiles are**:
    PRECONDITIONS: tst: ['3048', '3049', '3123'],
    PRECONDITIONS: stg: ['16576', '16575', '16602'],
    PRECONDITIONS: prod: ['28977', '28975', '29346']
    PRECONDITIONS: **'classId'** default value is **285** (for Horse Racing) and **286** (for Greyhounds)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Oxygen application is loaded
        """
        self.site.wait_content_state("Homepage")

    def test_002_on_homepage_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: On homepage tap 'Horse Racing' icon from the Sports Menu Ribbon
        EXPECTED: Horse Racing landing page is opened
        """
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.site.home.menu_carousel.items_as_ordered_dict.get(
                vec.sb.HORSERACING.upper() if self.brand == 'bma' else vec.sb.HORSERACING.title()).click()
        self.site.wait_content_state('Horseracing', timeout=5)
        if self.device_type == 'desktop':
            self.device.set_viewport_size(width=1600, height=1280)
            self.device.refresh_page()
            self.site.wait_splash_to_hide()

    def test_003_navigate_to_the_inspired_virtual_race_module(self):
        """
        DESCRIPTION: Navigate to the 'Inspired Virtual race' module
        EXPECTED: 'Inspired Virtual race' module is shown as Carousel
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Failed to display any section')
        if 'VIRTUAL RACE CAROUSEL' not in sections.keys():
            raise SiteServeException('"No Virtual Race Carousel" found as data was not available')
        self.assertTrue(sections['VIRTUAL RACE CAROUSEL'], msg='"VIRTUAL RACE CAROUSEL" is not shown')
        self.__class__.section = sections['VIRTUAL RACE CAROUSEL']
        self.section.scroll_to()

    def test_004_verify_hr_virtual_carousel_module(self):
        """
        DESCRIPTION: Verify 'HR Virtual Carousel' module
        EXPECTED: 'HR Virtual Carousel' module is expanded by default and may be collapsed/expanded once tapped
        """
        is_expanded = self.section.is_expanded()
        self.assertTrue(is_expanded, msg='"VIRTUAL RACE CAROUSEL" is not expanded by default')

    def test_005_verify_the_meetings_within_inspired_virtual_carousel(self):
        """
        DESCRIPTION: Verify the meetings within 'Inspired Virtual' carousel
        EXPECTED: - Header with name of meeting
        EXPECTED: - Start time of the race
        EXPECTED: - Count down timer for the video to start (for events that are not yet started)
        EXPECTED: - 'LIVE' badge instead of countdown timer (appears when eventStartTime + 1min20 sec.)
        EXPECTED: - 'BET NOW' clickable link for the events that are not yet started
        EXPECTED: - For events with 'Live' badge > the whole meeting area is clickable
        EXPECTED: - Only 5 next races are available within the carousel
        EXPECTED: - The last one is card with 'View all virtual events' clickable link
        EXPECTED: - Meetings may be swiped left/right within the carousel
        EXPECTED: **For tablet/desktop:**
        EXPECTED: - Meetings may be swiped left/right within the carousel using hover over arrows
        EXPECTED: - When first/last card is shown left/right hover over arrow is not shown
        """
        events = self.section.virtual_race_carousel.items_as_ordered_dict
        self.assertTrue(len(events) <= 5, msg='More than 5 races are displayed within the carousel')
        for event in events.values():
            start_time = wait_for_result(lambda: event.start_time.text is not None,
                                         name=f'start time to be displayed',
                                         timeout=10)
            live_label = event.live_label
            start_time_counter = event.start_time_counter
            bet_now_link = event.bet_now_link
            event_name = wait_for_result(lambda: event.name is not None, timeout=10)
            self.assertTrue(event_name, msg='No header with meeting name is displayed')
            self.assertTrue(start_time, msg=f'"{start_time}"No start time displayed')
            self.assertTrue(bet_now_link, msg='No "BET NOW LINK" displayed')
            if live_label:
                self.assertEqual(live_label.text, "LIVE", msg=f'Actual text "{live_label.text}" is not same as Expected text "LIVE"')
            else:
                self.assertTrue(start_time_counter, msg='No start time counter is displayed')
        if self.device_type == 'desktop':
            view_all_virtuals_link = self.section.virtual_race_carousel.view_all_virtuals_link
            self.assertTrue(view_all_virtuals_link, msg='"VIEW ALL VIRTUALS" link is not displayed')
