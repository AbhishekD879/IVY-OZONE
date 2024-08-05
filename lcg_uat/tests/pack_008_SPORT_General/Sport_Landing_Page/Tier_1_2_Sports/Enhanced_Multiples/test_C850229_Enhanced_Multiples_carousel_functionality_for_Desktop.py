import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod //cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C850229_Enhanced_Multiples_carousel_functionality_for_Desktop(Common):
    """
    TR_ID: C850229
    NAME: Enhanced Multiples carousel functionality for Desktop
    DESCRIPTION: This test case verifies Enhanced Multiples carousel functionality for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Make sure you have  Enhanced Multiples events on some sports (Sports events with typeName="Enhanced Multiples")
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. Enhanced Multiples are not available for Lotto and Virtuals.
    PRECONDITIONS: 2. Enhanced Multiples layout remains unchanged for tablet and mobile (EM events are displayed in accordions).
    PRECONDITIONS: 3. For each Class retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: XXX - is a comma-separated list of **Class **ID's;
    PRECONDITIONS: XX - sports **Category **ID
    PRECONDITIONS: X.XX - current supported version of the OpenBet release
    PRECONDITIONS: ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football enhanced multiples event
        """
        self.ob_config.add_football_event_enhanced_multiples()
        self.ob_config.add_football_event_enhanced_multiples()
        self.ob_config.add_football_event_enhanced_multiples()
        event_params3 = self.ob_config.add_football_event_enhanced_multiples()
        self.__class__.event_id = event_params3.event_id
        self.__class__.type_id = self.ob_config.football_config.specials.enhanced_multiples.type_id

    def test_001_navigate_to_any_sports_page_where_enhanced_multiples_events_are_present(self):
        """
        DESCRIPTION: Navigate to any <Sports> page where Enhanced Multiples events are present
        EXPECTED: • <Sports> Landing Page is opened
        EXPECTED: • 'Today' tab is selected by default
        EXPECTED: • 'Enhanced Multiples' events are displayed in carousel below the banner area
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        actual_date_tab_name = self.site.football.date_tab.current_date_tab
        self.assertEqual(actual_date_tab_name, vec.sb.SPORT_DAY_TABS.today,
                         msg=f'Actual date tab is "{actual_date_tab_name}" not "{vec.sb.SPORT_DAY_TABS.today}"')
        self.__class__.em_carousel = self.site.football.sport_enhanced_multiples_carousel
        self.assertTrue(self.em_carousel, msg='Enhanced Multiples carousel is not displayed')

    def test_002_hover_over_the_carousel(self):
        """
        DESCRIPTION: Hover over the carousel
        EXPECTED: Right arrow appears on the right side of carousel
        """
        self.em_carousel.mouse_over()
        self.assertTrue(self.site.football.has_right_arrow, msg='right arrow is not displayed')

    def test_003_click_on_the_right_arrow(self):
        """
        DESCRIPTION: Click on the right arrow
        EXPECTED: Content scrolls right
        """
        self.site.football.right_arrow.click()

    def test_004_hover_over_the_carousel_again(self):
        """
        DESCRIPTION: Hover over the carousel again
        EXPECTED: Right and left arrows appear on the sides of carousel respectively
        """
        self.em_carousel.mouse_over()
        self.assertTrue(self.site.football.has_right_arrow, msg='right arrow is not displayed')
        self.assertTrue(self.site.football.has_left_arrow, msg='left arrow is not displayed')

    def test_005_click_on_the_left_arrow(self):
        """
        DESCRIPTION: Click on the left arrow
        EXPECTED: Content scrolls left
        """
        self.site.football.left_arrow.click()

    def test_006_click_on_right_arrow_till_the_end_of_carousel(self):
        """
        DESCRIPTION: Click on right arrow till the end of carousel
        EXPECTED: • Carousel is not a loop, user is able to get to last 'Enhanced Multiples' event card
        EXPECTED: • Right arrow is not displayed at the end of carousel
        EXPECTED: • The last EM card is displayed at the end of carousel
        """
        while self.site.football.has_right_arrow:
            self.site.football.right_arrow.click()
            sleep(2)
        else:
            self.assertFalse(self.site.football.has_right_arrow, msg='right arrow is displayed')

        enhanced_section = list(self.site.football.sport_enhanced_multiples_carousel.items_as_ordered_dict.values())[-1]
        self.assertTrue(enhanced_section.outcome_name.is_displayed(), msg='last card is not displayed')

        self.em_carousel.mouse_over()
        while self.site.football.has_left_arrow:
            self.site.football.left_arrow.click()
            sleep(2)
        else:
            self.assertFalse(self.site.football.has_left_arrow, msg='left arrow is displayed')

    def test_007_choose_tomorrow_tab(self):
        """
        DESCRIPTION: Choose 'Tomorrow' tab
        EXPECTED: • The EM carousel is still displaying with all available outcomes
        EXPECTED: • The EM carousel is not reloaded during navigation between days (Today/Tomorrow/Future)
        """
        self.site.football.date_tab.tomorrow.click()
        self.__class__.em_carousel = self.site.football.sport_enhanced_multiples_carousel
        self.assertTrue(self.em_carousel, msg='Enhanced Multiples carousel is not displayed')

    def test_008_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps 2-6
        EXPECTED:
        """
        self.test_002_hover_over_the_carousel()
        self.test_003_click_on_the_right_arrow()
        self.test_004_hover_over_the_carousel_again()
        self.test_005_click_on_the_left_arrow()
        self.test_006_click_on_right_arrow_till_the_end_of_carousel()

    def test_009_choose_future_tab(self):
        """
        DESCRIPTION: Choose 'Future' tab
        EXPECTED: • The EM carousel is still displaying with all available outcomes
        EXPECTED: • The EM carousel is not reloaded during navigation between days (Today/Tomorrow/Future)
        """
        self.site.football.date_tab.future.click()
        self.__class__.em_carousel = self.site.football.sport_enhanced_multiples_carousel
        self.assertTrue(self.em_carousel, msg='Enhanced Multiples carousel is not displayed')

    def test_010_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps 2-6
        EXPECTED:
        """
        self.test_008_repeat_steps_2_6()

    def test_011_repeat_steps_2_6_on_sports_event_details_page_but_only_for_pre_match_events(self):
        """
        DESCRIPTION: Repeat steps 2-6 on <Sports> Event Details Page but only for Pre-match events
        EXPECTED:
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        sleep(5)
        self.__class__.em_carousel = self.site.football.sport_enhanced_multiples_carousel
        self.assertTrue(self.em_carousel, msg='Enhanced Multiples carousel is not displayed')
        self.test_008_repeat_steps_2_6()

    def test_012_repeat_steps_2_6_on_homepage(self):
        """
        DESCRIPTION: Repeat steps 2-6 on Homepage
        EXPECTED:
        """
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')
        self.__class__.em_carousel = self.site.home.desktop_modules.enhanced_module
        self.assertTrue(self.em_carousel, msg='Enhanced Multiples carousel is not displayed')
        self.em_carousel.mouse_over()
        self.assertTrue(self.site.home.desktop_modules.has_right_arrow, msg='right arrow is not displayed')
        self.site.home.desktop_modules.right_arrow.click()
        self.em_carousel.mouse_over()
        self.assertTrue(self.site.home.desktop_modules.has_right_arrow, msg='right arrow is not displayed')
        self.assertTrue(self.site.home.desktop_modules.has_left_arrow, msg='left arrow is not displayed')
        while self.site.home.desktop_modules.has_right_arrow:
            self.site.home.desktop_modules.right_arrow.click()
            sleep(2)
        else:
            self.assertFalse(self.site.home.desktop_modules.has_right_arrow, msg='right arrow is displayed')
        enhanced_section = list(self.site.home.desktop_modules.enhanced_module.items_as_ordered_dict.values())[-1]
        self.assertTrue(enhanced_section.outcome_name.is_displayed(), msg='last card is not displayed')
