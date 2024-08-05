import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from time import sleep
from selenium.common.exceptions import StaleElementReferenceException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot create events in prod/beta
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C1049075_Carousel_functionality_on_In_play_widget_for_Desktop(BaseCashOutTest):
    """
    TR_ID: C1049075
    NAME: Carousel functionality on In-play widget for Desktop
    DESCRIPTION: This test case verifies carousel functionality on In-play widget for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        """
        try:
            live_events = self.get_active_events_for_category(category_id=24, in_play_event=True, all_available_events=True)
            for event in live_events:
                self.ob_config.change_event_state(event_id=event['event']['id'])
        except SiteServeException:
            self._logger.info('no live events found')
        self.__class__.event_id = self.ob_config.add_formula_1_event(is_live=True).event_id
        self.create_several_autotest_premier_league_football_events(is_live=True, number_of_events=4)

    def test_001_navigate_to_any_sports_landing_page_that_contains_several_live_events(self):
        """
        DESCRIPTION: Navigate to any Sports Landing page that contains several Live events
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is displayed
        EXPECTED: * In-Play widget is expanded by default
        EXPECTED: * Live events are displayed in the carousel
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state('FOOTBALL')
        self.__class__.section = self.site.football.in_play_widget.items_as_ordered_dict.get('In-Play LIVE Football')
        self.assertTrue(self.section, msg='"In-Play" widget not found on SLP')
        self.assertTrue(self.section.is_expanded(), msg='"In-Play" widget is not expanded by default')
        self.__class__.events = self.section.content.items_as_ordered_dict
        self.assertTrue(self.events, msg='events are not displayed')

    def test_002_hover_over_the_carousel(self):
        """
        DESCRIPTION: Hover over the carousel
        EXPECTED: The right arrow appears on the right side of carousel
        """
        event1 = list(self.events.values())[0]
        event1.mouse_over()
        sleep(1)
        self.__class__.right_arrow = self.section.right_arrow
        self.assertTrue(self.right_arrow.is_displayed(), msg='Right arrow not displayed after mouse over on the carousel')

    def test_003_click_on_the_right_arrow(self):
        """
        DESCRIPTION: Click on the right arrow
        EXPECTED: * Content scrolls right
        EXPECTED: * Current set of event cards are replaced by the same number of the next cards
        """
        self.right_arrow.click()
        event2 = list(self.events.values())[1]
        event2.mouse_over()
        sleep(1)
        self.__class__.left_arrow = self.section.left_arrow
        self.assertTrue(self.right_arrow.is_displayed(), msg='Right arrow not displayed after mouse over on the carousel')
        self.assertTrue(self.left_arrow.is_displayed(), msg='Left arrow not displayed after mouse over on the carousel')

    def test_004_hover_over_the_carousel_again(self):
        """
        DESCRIPTION: Hover over the carousel again
        EXPECTED: Right and left arrows appear on the sides of carousel respectively
        """
        # covered in step 003

    def test_005_click_on_the_left_arrow(self):
        """
        DESCRIPTION: Click on the left arrow
        EXPECTED: * Content scrolls left
        EXPECTED: * Current set of event cards are replaced by the same number of the next cards
        """
        self.left_arrow.click()
        sleep(1)
        try:
            self.assertFalse(self.left_arrow.is_displayed(), msg='Content not scrolled to left as there is left arrow')
        except StaleElementReferenceException:
            self._logger.info('Content scrolled to left as there is not left arrow')

    def test_006_click_on_right_arrow_till_the_end_of_carousel(self):
        """
        DESCRIPTION: Click on right arrow till the end of carousel
        EXPECTED: * Carousel is not a loop, user is able to get to last Live event card
        EXPECTED: * Right arrow is not displayed at the end of carousel
        EXPECTED: * The last Live event card is displayed at the end of carousel
        """
        for _ in range(len(self.events) - 1):
            self.right_arrow.click()
        sleep(1)
        try:
            self.assertFalse(self.right_arrow.is_displayed(), msg='Right arrow is still present at the end of carousel')
        except StaleElementReferenceException:
            self._logger.info('Content scrolled to left as there is not left arrow')

    def test_007_navigate_to_any_sports_landing_page_that_contains_only_one_live_event(self):
        """
        DESCRIPTION: Navigate to any Sports Landing page that contains only one Live event
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is displayed
        EXPECTED: * In-Play widget is expanded by default
        EXPECTED: * Only one card is displayed within carousel on the whole width of the In-Play widget
        EXPECTED: * Right/left arrows are NOT shown on the sides of carousel
        """
        self.__class__.sport_name = self.get_sport_title(category_id=24)
        self.site.open_sport(self.sport_name)
        section = self.site.formula_1.in_play_widget.items_as_ordered_dict.get('In-Play LIVE Formula1')
        self.assertTrue(section, msg='"In-Play" widget not found on SLP')
        self.assertTrue(section.is_expanded(), msg='"In-Play" widget is not expanded by default')
        events = section.content.items_as_ordered_dict
        self.assertEqual(len(list(events.values())), 1, msg='events are not displayed')
        event1 = list(events.values())[0]
        event1.mouse_over()
        sleep(1)
        right_arrow = section.right_arrow
        self.assertFalse(right_arrow, msg='Right arrow is displayed when there is only one live event')
        left_arrow = section.left_arrow
        self.assertFalse(left_arrow, msg='left arrow is displayed when there is only one live event')

    def test_008_navigate_to_any_sports_landing_page_that_doesnt_contain_any_live_events(self):
        """
        DESCRIPTION: Navigate to any Sports Landing page that doesn't contain any Live events
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is NOT displayed
        """
        self.ob_config.change_event_state(event_id=self.event_id)
        self.device.refresh_page()
        sleep(1)
        self.assertFalse(self.site.formula_1.in_play_widget.is_displayed(), msg='In-Play widget is still displaying when there are no live events')
