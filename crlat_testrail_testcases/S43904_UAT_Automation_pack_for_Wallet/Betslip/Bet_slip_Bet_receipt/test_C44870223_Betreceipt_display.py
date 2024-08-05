import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870223_Betreceipt_display(Common):
    """
    TR_ID: C44870223
    NAME: Betreceipt display
    DESCRIPTION: 
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True

    def test_001_log_in_on_desktop_siteapp(self):
        """
        DESCRIPTION: Log in on desktop site/App
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_a_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add a selections to the Bet slip
        EXPECTED: The selections are added to the Bet slip
        """
        pass

    def test_003_enter_a_stake(self):
        """
        DESCRIPTION: Enter a stake
        EXPECTED: The stakes are displayed on the Bet slip
        """
        pass

    def test_004_click_on_place_bet(self):
        """
        DESCRIPTION: Click on Place Bet
        EXPECTED: The bet is placed successfully and the Receipt is displayed
        """
        pass

    def test_005_check_that_bet_details_are_correctly_displayed(self):
        """
        DESCRIPTION: Check that bet details are correctly displayed
        EXPECTED: User should see the bellow details
        EXPECTED: *bet id
        EXPECTED: *selection name
        EXPECTED: *market name / event name
        EXPECTED: *Cash out available icon when available
        EXPECTED: *Check display of estimated returns' / 'potential returns' for that individual bet
        EXPECTED: * Check display of'total stake' / 'stake for this bet' for that individual bet
        EXPECTED: * Check header balance update after placing bet
        EXPECTED: * Check my bets and bet history.
        """
        pass
