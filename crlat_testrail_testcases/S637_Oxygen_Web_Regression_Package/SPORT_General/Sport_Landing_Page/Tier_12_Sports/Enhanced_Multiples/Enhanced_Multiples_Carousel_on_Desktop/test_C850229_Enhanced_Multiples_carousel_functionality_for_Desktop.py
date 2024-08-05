import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
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

    def test_001_navigate_to_any_sports_page_where_enhanced_multiples_events_are_present(self):
        """
        DESCRIPTION: Navigate to any <Sports> page where Enhanced Multiples events are present
        EXPECTED: • <Sports> Landing Page is opened
        EXPECTED: • 'Today' tab is selected by default
        EXPECTED: • 'Enhanced Multiples' events are displayed in carousel below the banner area
        """
        pass

    def test_002_hover_over_the_carousel(self):
        """
        DESCRIPTION: Hover over the carousel
        EXPECTED: Right arrow appears on the right side of carousel
        """
        pass

    def test_003_click_on_the_right_arrow(self):
        """
        DESCRIPTION: Click on the right arrow
        EXPECTED: Content scrolls right
        """
        pass

    def test_004_hover_over_the_carousel_again(self):
        """
        DESCRIPTION: Hover over the carousel again
        EXPECTED: Right and left arrows appear on the sides of carousel respectively
        """
        pass

    def test_005_click_on_the_left_arrow(self):
        """
        DESCRIPTION: Click on the left arrow
        EXPECTED: Content scrolls left
        """
        pass

    def test_006_click_on_right_arrow_till_the_end_of_carousel(self):
        """
        DESCRIPTION: Click on right arrow till the end of carousel
        EXPECTED: • Carousel is not a loop, user is able to get to last 'Enhanced Multiples' event card
        EXPECTED: • Right arrow is not displayed at the end of carousel
        EXPECTED: • The last EM card is displayed at the end of carousel
        """
        pass

    def test_007_choose_tomorrow_tab(self):
        """
        DESCRIPTION: Choose 'Tomorrow' tab
        EXPECTED: • The EM carousel is still displaying with all available outcomes
        EXPECTED: • The EM carousel is not reloaded during navigation between days (Today/Tomorrow/Future)
        """
        pass

    def test_008_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps 2-6
        EXPECTED: 
        """
        pass

    def test_009_choose_future_tab(self):
        """
        DESCRIPTION: Choose 'Future' tab
        EXPECTED: • The EM carousel is still displaying with all available outcomes
        EXPECTED: • The EM carousel is not reloaded during navigation between days (Today/Tomorrow/Future)
        """
        pass

    def test_010_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps 2-6
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_2_6_on_sports_event_details_page_but_only_for_pre_match_events(self):
        """
        DESCRIPTION: Repeat steps 2-6 on <Sports> Event Details Page but only for Pre-match events
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_2_6_on_homepage(self):
        """
        DESCRIPTION: Repeat steps 2-6 on Homepage
        EXPECTED: 
        """
        pass
