import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C1364022_Check_again_after_switcher_removingTypes_accordions_scroll_and_expandability_after_switch_between_Live_now_and_Upcoming_filters(Common):
    """
    TR_ID: C1364022
    NAME: [Check again after switcher removing]Types accordions scroll and expandability after switch between "Live now" and "Upcoming" filters
    DESCRIPTION: This test case verifies the display, scroll and expandabilty of types' accordions after switch between "Live now" and "Upcoming" filters
    PRECONDITIONS: Test case requires TI and CMS configuration for adding/removing types on In Play page for different sports
    PRECONDITIONS: In order to have event on In Play page of some sport the following should be configured in TI:
    PRECONDITIONS: 1. Event should be in-Play: in TI check "Bet In Play list" on the event level
    PRECONDITIONS: 2. Event should also have a primary market defined to be shown on In Play tab (check in devlog): <Football, Tennis> - Match Betting market, <Basketball, American football, Ice hockey, Baseball> - Money line market, <Rugby, Cricket> - Match Betting market
    PRECONDITIONS: 3. Event should have "Bet In Running" checked on the market level
    PRECONDITIONS: 4. To display event under "Live now" filter: IsOff = Yes in TI on the event level . To display event under "Upcoming" filter: IsOff = N/A or NO in TI on the event level
    PRECONDITIONS: The number of accordions expanded by defaut is set in the CMS:
    PRECONDITIONS: System configuration > InPlayCompetitionsExpanded (competitionsCount value). Set value "2" for this test case
    PRECONDITIONS: Check the test with the different number of type accordions expanded by default.
    """
    keep_browser_open = True

    def test_001_configure_ti_to_have_nothing_displayed_under_live_filter_and_5_or_more_types_accordions_to_be_displayed_under_upcoming_filternavigate_to_sport_in_play_tab_scroll_down_and_expand_collapsed_accordions(self):
        """
        DESCRIPTION: Configure TI to have nothing displayed under Live filter and 5 or more types accordions to be displayed under "Upcoming" filter.
        DESCRIPTION: Navigate to sport In Play tab, scroll down and expand collapsed accordions
        EXPECTED: - "Upcoming" filter is selected
        EXPECTED: - Types' accordions list can be scrolled and accordions expanded/collapsed
        """
        pass

    def test_002_switch_to_the_live_now_filter_and_back_to_upcoming_filterscroll_down_and_expand_collapsed_accordions(self):
        """
        DESCRIPTION: Switch to the "Live now" filter and back to "Upcoming" filter.
        DESCRIPTION: Scroll down and expand collapsed accordions
        EXPECTED: - Message "There are currently no Live events available" on the empty "Live now" filter
        EXPECTED: - "Upcoming" filter is selected
        EXPECTED: - Types' accordions list can be scrolled and accordions expanded/collapsed
        """
        pass

    def test_003_configure_ti_to_have_nothing_displayed_under_upcoming_filter_and_5_or_more_types_accordions_to_be_displayed_under_live_filternavigate_to_sport_in_play_tab_scroll_down_and_expand_collapsed_accordions(self):
        """
        DESCRIPTION: Configure TI to have nothing displayed under "Upcoming" filter and 5 or more types accordions to be displayed under "Live" filter.
        DESCRIPTION: Navigate to sport In Play tab, scroll down and expand collapsed accordions
        EXPECTED: - "Live now" filter is selected
        EXPECTED: - Types' accordions list can be scrolled and accordions expanded/collapsed
        """
        pass

    def test_004_switch_to_upcoming_filter_and_back_to_live_now_filterscroll_down_and_expand_collapsed_accordions(self):
        """
        DESCRIPTION: Switch to "Upcoming filter" and back to "Live now" filter
        DESCRIPTION: Scroll down and expand collapsed accordions
        EXPECTED: - Message "There are currently no Live events available" on the empty "Upcoming" filter
        EXPECTED: - "Live now" filter is selected
        EXPECTED: - Types' accordions list can be scrolled and accordions expanded/collapsed
        """
        pass

    def test_005_configure_ti_to_have_5_or_more_types_accordions_displayed_under_live_filter_and_5_or_more_types_accordions_displayed_under_upcoming_filternavigate_to_sport_in_play_tab_scroll_down_and_expand_collapsed_accordions(self):
        """
        DESCRIPTION: Configure TI to have 5 or more types accordions displayed under Live filter and 5 or more types accordions displayed under "Upcoming" filter.
        DESCRIPTION: Navigate to sport In Play tab, scroll down and expand collapsed accordions
        EXPECTED: - "Live now" filter is selected
        EXPECTED: - Types' accordions list can be scrolled and accordions expanded/collapsed
        """
        pass

    def test_006_switch_to_upcoming_filterscroll_down_and_expand_collapsed_accordions(self):
        """
        DESCRIPTION: Switch to "Upcoming" filter.
        DESCRIPTION: Scroll down and expand collapsed accordions
        EXPECTED: - "Upcoming" filter is selected
        EXPECTED: - Types' accordions list can be scrolled and accordions expanded/collapsed
        """
        pass
