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
class Test_C1696995_Banach_Markets_with_1_switcher_90min_1st_2nd_Half_3_x_Selections_positive_cases(Common):
    """
    TR_ID: C1696995
    NAME: Banach. Markets with 1 switcher (90min, 1st, 2nd Half) & 3 x Selections (positive cases)
    DESCRIPTION: This test case verifies positive cases in functionality of switcher (90min, 1st, 2nd Half) on 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab on EDP of event
    DESCRIPTION: Test case should be run after [Trigger selections dashboard and price][1] is passed
    DESCRIPTION: [1]: https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    PRECONDITIONS: **Build Your Bet CMS configuration:**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Scope of markets with 1 switcher (90min, 1st, 2nd Half) & 3 x Selections. Select available for testing**
    PRECONDITIONS: MATCH BETTING,
    PRECONDITIONS: CORNERS MATCH BET,
    PRECONDITIONS: BOOKINGS MATCH BET,
    PRECONDITIONS: DOUBLE CHANCE
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: **'Build Your Bet/Bet Builder' tab on event details page is loaded and no selections are added to the dashboard**
    """
    keep_browser_open = True

    def test_001_click_on_market_headers_match_betting(self):
        """
        DESCRIPTION: Click on market headers 'MATCH BETTING'
        EXPECTED: Switcher with three tabs is displayed:
        EXPECTED: * '90 MIN' (selected by default)
        EXPECTED: * '1ST HALF'
        EXPECTED: * '2ND HALF'
        """
        pass

    def test_002_tap_on_each_tab_of_the_switchers_90_min__1st_half__2nd_half(self):
        """
        DESCRIPTION: Tap on each tab of the switchers '90 MIN' / '1ST HALF' / '2ND HALF'.
        EXPECTED: Three selections (e.g. 'Burnley', 'Draw', 'Stoke') is offered as the buttons below each switcher (as per **selections request** mentioned in preconditions).
        """
        pass

    def test_003_tap_on_the_selection_eg_burnley_from_one_of_the_switcher_tabs_eg_1st_half(self):
        """
        DESCRIPTION: Tap on the selection (e.g. 'Burnley') from one of the switcher tabs (e.g. '1ST HALF')
        EXPECTED: * Selection is highlighted inside accordion.
        EXPECTED: * Selection is added to the dashboard.
        """
        pass

    def test_004_tap_on_the_selection_eg_draw_from_different_tab_eg_2nd_half(self):
        """
        DESCRIPTION: Tap on the selection (e.g. 'Draw') from different tab (e.g. '2ND HALF')
        EXPECTED: * Selection is highlighted inside accordion.
        EXPECTED: * Selection is added to the dashboard (2 selections are present in the dashboard).
        """
        pass

    def test_005_tap_on_different_selection_eg_stoke_from_the_same_switcher_tab_eg_2nd_half(self):
        """
        DESCRIPTION: Tap on different selection (e.g. 'Stoke') from the same switcher tab (e.g. '2ND HALF')
        EXPECTED: * Selection is highlighted inside accordion.
        EXPECTED: * Previous selection from the same tab has been substituted with the new selection in the dashboard (2 selections are present in the dashboard )
        """
        pass
