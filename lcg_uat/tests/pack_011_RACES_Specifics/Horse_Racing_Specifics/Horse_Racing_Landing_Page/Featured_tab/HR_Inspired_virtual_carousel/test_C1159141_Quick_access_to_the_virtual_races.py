import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.js_functions import click



@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1159141_Quick_access_to_the_virtual_races(Common):
    """
    TR_ID: C1159141
    NAME: Quick access to the virtual races
    DESCRIPTION: This test case verifies quick access for the virtual race module
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
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.sb.HORSERACING.upper() if self.brand == 'bma' else vec.sb.HORSERACING.title()).click()
        self.site.wait_content_state('Horseracing', timeout=8)

    def test_003_navigate_to_the_inspired_virtual_race_module(self):
        """
        DESCRIPTION: Navigate to the 'Inspired Virtual race' module
        EXPECTED: 'Inspired Virtual race' module is shown as Carousel module
        """
        try:
            sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        except:
            self.device.refresh_page()
            sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Failed to display any section')
        if 'VIRTUAL RACE CAROUSEL' not in sections.keys():
            raise SiteServeException('"No Virtual Race Carousel" found as data was not available')
        self.assertTrue(sections['VIRTUAL RACE CAROUSEL'], msg='"VIRTUAL RACE CAROUSEL" is not shown')
        self.__class__.section = sections['VIRTUAL RACE CAROUSEL']
        self.section.scroll_to()

    def test_004_click_on_the_bet_now_link_of_a_meeting_card_with_available_count_down_timer(self):
        """
        DESCRIPTION: Click on the 'Bet Now' link of a meeting card with available count down timer
        EXPECTED: User is redirected to a corresponding event details on 'Inspired virtual' page
        """
        events = self.section.virtual_race_carousel.items_as_ordered_dict
        if len(events) > 2:
            sleep(2)
            bet_now_link = list(events.values())[2].bet_now_link
            bet_now_link.scroll_to()
            bet_now_link.click()
            self.site.wait_content_state('VIRTUAL', timeout=5)

    def test_005_go_back_to_hr_landing_page__click_on_the_meeting_card_with_available_live_badge(self):
        """
        DESCRIPTION: Go back to HR landing page > Click on the meeting card with available 'LIVE' badge
        EXPECTED: - User is redirected to a corresponding event details on 'Inspired virtual' page
        EXPECTED: -  If video stream of an event has already ended and "evenIsOff" time =45 sec (see preconditions) has not yet passed, warning message is shown on the red background on event details page: "Requested race is OFF and we propose to see the following:"
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing', timeout=5)
        try:
            sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        except:
            self.device.refresh_page()
            sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        if 'VIRTUAL RACE CAROUSEL' not in sections.keys():
            raise SiteServeException('"No Virtual Race Carousel" found as data was not available')
        section = sections['VIRTUAL RACE CAROUSEL']
        section.scroll_to()
        if not section.is_expanded() :
            section.expand()
        events = section.virtual_race_carousel.items_as_ordered_dict
        has_live_lable = list(events.values())[0].has_live_label()
        if has_live_lable:
            sleep(2)
            live_label = list(events.values())[0].live_label
            live_label.click()
            self.site.wait_content_state('VIRTUAL', timeout=5)
        # Can't verify video stream of an event

    def test_006_go_back_to_hr_landing_page__swipe_to_the_last_view_all_virtual_events_card__tap_on_the__view_all_virtual_events_link(self):
        """
        DESCRIPTION: Go back to HR landing page > Swipe to the last 'View all virtual events' card > Tap on the  'View all virtual events' link
        EXPECTED: User is redirected to the 'Inspired virtual' page > first available event details tab
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing', timeout=8)
        try:
            sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        except:
            self.device.refresh_page()
            sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        if 'VIRTUAL RACE CAROUSEL' not in sections.keys():
            raise SiteServeException('"No Virtual Race Carousel" found as data was not available')
        section = sections['VIRTUAL RACE CAROUSEL']
        section.scroll_to()
        if not section.is_expanded():
            section.expand()
        sleep(2)
        view_all_virtuals_link = section.virtual_race_carousel.view_all_virtuals_link
        click(view_all_virtuals_link)
        self.site.wait_content_state('VIRTUAL', timeout=5)
