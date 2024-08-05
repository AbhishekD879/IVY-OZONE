import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.sports
@vtest
class Test_C874352_Navigation_Football(Common):
    """
    TR_ID: C874352
    NAME: Navigation Football
    DESCRIPTION: Test case verifies navigation through Football pages is correct:
    DESCRIPTION: Matches
    DESCRIPTION: Coupons
    DESCRIPTION: Outrights
    DESCRIPTION: Specials
    DESCRIPTION: Enhanced Multiples
    DESCRIPTION: Event Details page
    DESCRIPTION: Combined Markets
    DESCRIPTION: if 'Coupons' Tab is not available see instruction how to generate [Coupon](https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system)
    DESCRIPTION: AUTOMATED [C45194871] [C45766219]
    PRECONDITIONS: Open Oxygen app
    """
    keep_browser_open = True

    def test_001_click_on_football_button_from_the_main_menu(self):
        """
        DESCRIPTION: Click on Football button from the Main Menu
        EXPECTED: 1. Football Page is loaded
        EXPECTED: 2. The Matches tab is selected by default
        EXPECTED: 3. The first 3 Leagues are expanded by default, and the rest of them are collapsed
        EXPECTED: 4. All events which are available are displayed for the League
        EXPECTED: 5. The "Match Result" option is selected in the market selector for all the event types
        EXPECTED: 6. **For Mobile/Tablet:**
        EXPECTED: Enhanced Multiple events section (if available) is displayed on the top of the list and is expanded
        EXPECTED: **For Desktop:**
        EXPECTED: Enhanced Multiple events section (if available) is displayed as carousel above tabs
        EXPECTED: 7. **For Desktop:**
        EXPECTED: 'In-Play' widget is displayed in 3rd column or below main content (depends on screen resolution) with live events in carousel
        """
        pass

    def test_002_select_a_different_option_from_the_market_selector_eg_total_goals_overunder_25(self):
        """
        DESCRIPTION: Select a different option from the market selector (e.g. "Total Goals Over/Under 2.5")
        EXPECTED: The events list is updated automatically
        EXPECTED: The "Total Goals Over/Under 2.5" selections are now displayed in the list for the events from this Event Type
        """
        pass

    def test_003_click_on_competitions_tab(self):
        """
        DESCRIPTION: Click on Competitions tab
        EXPECTED: 1. The Competition Page is loaded
        EXPECTED: 2. The first Competition is expanded by default (the rest of them are collapsed)
        """
        pass

    def test_004_select_one_event_from_the_competitions_tab(self):
        """
        DESCRIPTION: Select one event from the competitions tab
        EXPECTED: The list of events from that competition is displayed
        """
        pass

    def test_005_click_on_back_button_and_then_click_on_coupons_tab(self):
        """
        DESCRIPTION: Click on Back Button and then click on Coupons Tab
        EXPECTED: List Of Coupons is displayed in 'Popular Coupons' and 'Featured Coupons' sections
        """
        pass

    def test_006_select_any_coupon_from_the_list(self):
        """
        DESCRIPTION: Select any coupon from the list
        EXPECTED: * Selected Coupon name is displayed on Subheader
        EXPECTED: * A list of the events available under the specific coupon is displayed
        EXPECTED: * Check that the "name" of the selections from the header are correct:
        EXPECTED: - Yes/No for "Both Teams to Score" coupon
        EXPECTED: - Over/Under for Over/Under 2.5 Coupon
        EXPECTED: - Home/Away for "To Win to Nil" coupon
        """
        pass

    def test_007_coral_only_tap_on_change_coupon_dropdown_on_subheader_and_select_any_other_coupon(self):
        """
        DESCRIPTION: **CORAL only:** Tap on 'Change Coupon' dropdown on subheader and select any other coupon
        EXPECTED: * Selected Coupon name is displayed on Subheader
        EXPECTED: * A list of the events available under the specific coupon is displayed
        EXPECTED: * Check that the "name" of the selections from the header are correct:
        EXPECTED: - Yes/No for "Both Teams to Score" coupon
        EXPECTED: - Over/Under for Over/Under 2.5 Coupon
        EXPECTED: - Home/Away for "To Win to Nil" coupon
        """
        pass

    def test_008_go_back_to_football_landing_page_and_click_on_outrights_tab(self):
        """
        DESCRIPTION: Go back to Football Landing page and Click on Outrights Tab
        EXPECTED: The Outrights tab is loaded
        EXPECTED: Leagues and Competitions are all collapsed by default
        """
        pass

    def test_009_expand_one_event_type(self):
        """
        DESCRIPTION: Expand one event type
        EXPECTED: The list of outrights from that event type are displayed
        """
        pass

    def test_010_click_on_specials_tab_if_available(self):
        """
        DESCRIPTION: Click on Specials tab (if available)
        EXPECTED: The Specials tab is loaded
        EXPECTED: The first event type is expanded by default (the rest of them are collapsed)
        """
        pass

    def test_011_click_on_in_play_tab(self):
        """
        DESCRIPTION: Click on In Play Tab
        EXPECTED: The In Play tab is loaded (with Live now, Upcoming sections)
        EXPECTED: The first N leagues are expanded by default (the rest of them are collapsed), N - CMS configurable value
        """
        pass
