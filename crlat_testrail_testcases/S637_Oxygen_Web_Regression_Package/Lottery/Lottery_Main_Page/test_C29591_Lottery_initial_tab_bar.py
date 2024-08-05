import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.lotto
@vtest
class Test_C29591_Lottery_initial_tab_bar(Common):
    """
    TR_ID: C29591
    NAME: Lottery initial tab bar
    DESCRIPTION: This test case verifies Lottery initial tab bar.
    DESCRIPTION: JIRA TICKETS:
    DESCRIPTION: BMA-7983: Lotto - Initial selection tab
    PRECONDITIONS: To get a list of lotteries and draws use following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/X.XX/LotteryToDraw/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    """
    keep_browser_open = True

    def test_001_load_oxygen_aplication(self):
        """
        DESCRIPTION: Load Oxygen aplication
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_lotto_page(self):
        """
        DESCRIPTION: Go to 'Lotto' page
        EXPECTED: 'Lotto' page is opened
        """
        pass

    def test_003_verify_lottery_initial_tab_bar(self):
        """
        DESCRIPTION: Verify Lottery initial tab bar
        EXPECTED: *   The following tabs are displayed in the tab bar at the top of the page (under the lottery product carousel):
        EXPECTED: 1.  'Straight'
        EXPECTED: 2.  'Combo'
        EXPECTED: 3.  'Result'
        EXPECTED: *   'Straight' tab is opened by default
        EXPECTED: *   All tabs are cllickable
        """
        pass

    def test_004_within_selected_lottery_switch_between_tabs_for_this_lottery(self):
        """
        DESCRIPTION: Within selected Lottery switch between tabs for this Lottery
        EXPECTED: Related information to the selected tab is loaded on the page
        """
        pass

    def test_005_go_to_comboresults_tabselect_any_other_lottery_from_lotto_carousel_ribbon(self):
        """
        DESCRIPTION: Go to Combo/Results tab.
        DESCRIPTION: Select any other Lottery from Lotto Carousel Ribbon
        EXPECTED: *   Previously opened Combo/Results tab is displayed for selected Lottery
        EXPECTED: *   Related information to selected Lottery is loaded on the page
        EXPECTED: *   The first 'Straight 'tab is NOT opened by default when changing Lottery
        """
        pass

    def test_006_open_any_tabs_within_selected_lottery(self):
        """
        DESCRIPTION: Open any tabs within selected Lottery
        EXPECTED: *   Previosly opened Lottery is still displayed
        EXPECTED: *   Related information to selected tab is loaded on the page
        EXPECTED: *   The first Lottery is NOT opened by default when changing tab
        """
        pass
