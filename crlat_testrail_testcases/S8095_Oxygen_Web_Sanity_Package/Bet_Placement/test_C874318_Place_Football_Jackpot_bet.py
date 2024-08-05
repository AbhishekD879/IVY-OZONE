import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C874318_Place_Football_Jackpot_bet(Common):
    """
    TR_ID: C874318
    NAME: Place Football Jackpot bet
    DESCRIPTION: AUTOTEST [C9690156]
    PRECONDITIONS: 1. Login to Oxygen
    """
    keep_browser_open = True

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: Football page is loaded
        """
        pass

    def test_002_navigate_to_jackpot_tab(self):
        """
        DESCRIPTION: Navigate to Jackpot tab
        EXPECTED: Football Jackpot page is loaded
        """
        pass

    def test_003_click_on_lucky_dip_button(self):
        """
        DESCRIPTION: Click on Lucky Dip button
        EXPECTED: One selection from each event is selected (total 15 selections)
        """
        pass

    def test_004_manually_select_one_random_selection(self):
        """
        DESCRIPTION: Manually select one random selection
        EXPECTED: Verify that the customer can manually edit the selections highlighted by the Lucky Dip button
        """
        pass

    def test_005_observe_the_default_selected_stake(self):
        """
        DESCRIPTION: Observe the default selected stake
        EXPECTED: The default selected stake is £1.00
        """
        pass

    def test_006_click_on_bet_now_button(self):
        """
        DESCRIPTION: Click on Bet Now button
        EXPECTED: The bet is successfully placed.
        """
        pass

    def test_007_check_bet_receipt(self):
        """
        DESCRIPTION: Check Bet receipt
        EXPECTED: All information is correct
        EXPECTED: **to update this whenever bet placement will be fixed
        """
        pass
