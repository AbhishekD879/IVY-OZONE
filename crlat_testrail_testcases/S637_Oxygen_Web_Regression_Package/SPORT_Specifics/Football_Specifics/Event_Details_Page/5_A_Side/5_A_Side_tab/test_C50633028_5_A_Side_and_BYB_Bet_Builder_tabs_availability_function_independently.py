import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C50633028_5_A_Side_and_BYB_Bet_Builder_tabs_availability_function_independently(Common):
    """
    TR_ID: C50633028
    NAME: '5-A-Side'  and 'BYB/Bet Builder' tabs availability function independently
    DESCRIPTION: This test case verifies that '5-A-Side' and 'BYB/Bet Builder' tabs feature toggles function independently i.e. it's possible to set up the case when both tabs are shown and when only one of them is displayed
    PRECONDITIONS: **5-A-Side and BYB/Bet Builder configs:**
    PRECONDITIONS: - '5-A-Side' is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - 'BYB/Bet Builder' is enabled in CMS > System Configuration -> Structure -> YourCallIconsAndTabs -> enableTab
    PRECONDITIONS: - Banach league under test is added and enabled for 5-A-Side and BYB in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ and 'Active for BYB' are ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request  to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side and BYB/Bet Builder configs
    """
    keep_browser_open = True

    def test_001_verify_5_a_side_and_bet_builder_tabs(self):
        """
        DESCRIPTION: Verify '5-A-Side' and 'Bet Builder' tabs
        EXPECTED: Both tabs are displayed
        """
        pass

    def test_002__disable_5_a_side_tab_in_cms__system_configuration___structure___fiveaside_refresh_the_event_details_page_on_fe(self):
        """
        DESCRIPTION: * Disable '5-A-Side' tab in CMS > System Configuration -> Structure -> FiveASide
        DESCRIPTION: * Refresh the event details page on FE
        EXPECTED: * '5-A-Side' tab is NOT displayed
        EXPECTED: * 'Bet Builder' tab is displayed
        """
        pass

    def test_003__enable_5_a_side_in_cms__system_configuration___structure___fiveaside_disable_bet_builder_tab_in_cms__system_configuration___structure___yourcalliconsandtabs_refresh_the_event_details_page_on_fe(self):
        """
        DESCRIPTION: * Enable '5-A-Side' in CMS > System Configuration -> Structure -> FiveASide
        DESCRIPTION: * Disable 'Bet Builder' tab in CMS > System Configuration -> Structure -> YourCallIconsAndTabs
        DESCRIPTION: * Refresh the event details page on FE
        EXPECTED: * '5-A-Side' tab is displayed
        EXPECTED: * 'Bet Builder' tab is NOT displayed
        """
        pass

    def test_004__enable_both_tabs_in_cms__system_configuration_untick_active_for_5_a_side_in_cms___byb___banach_leagues___select_league_under_test_refresh_the_event_details_page_on_fe(self):
        """
        DESCRIPTION: * Enable both tabs in CMS > System Configuration
        DESCRIPTION: * Untick ‘Active for 5 A Side’ in CMS -> BYB -> Banach Leagues -> select league under test
        DESCRIPTION: * Refresh the event details page on FE
        EXPECTED: * '5-A-Side' tab is NOT displayed
        EXPECTED: * 'Bet Builder' tab is displayed
        """
        pass

    def test_005__tick_active_for_5_a_side_in_cms___byb___banach_leagues___select_league_under_test_untick_active_for_byb_in_cms___byb___banach_leagues___select_league_under_test_refresh_the_event_details_page_on_fe(self):
        """
        DESCRIPTION: * Tick ‘Active for 5 A Side’ in CMS -> BYB -> Banach Leagues -> select league under test
        DESCRIPTION: * Untick ‘Active for BYB’ in CMS -> BYB -> Banach Leagues -> select league under test
        DESCRIPTION: * Refresh the event details page on FE
        EXPECTED: * '5-A-Side' tab is displayed
        EXPECTED: * 'Bet Builder' tab is NOT displayed
        """
        pass
