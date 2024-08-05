import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C14890130_from_OX99_Betslip_verify_displaying_of_i_icon_for_for_Single_Stakes_and_Double_Stakes_About(Common):
    """
    TR_ID: C14890130
    NAME: [from OX99] Betslip: verify displaying of 'i' icon for for Single Stakes and Double Stakes About
    DESCRIPTION: This test case verifies displaying of 'i' icon for for Single Stakes and Double Stakes About
    PRECONDITIONS: Verify on environment with prod endpoint (also could be available on Desktop)
    PRECONDITIONS: Add 2 selections to the Betslip
    PRECONDITIONS: Go to the Betslip
    """
    keep_browser_open = True

    def test_001_verify_that_single_stakes_about_multiple_bet_and_double_stakes_about_multiple_bet_is_available_in_betslip(self):
        """
        DESCRIPTION: Verify that 'Single Stakes About' multiple bet and 'Double Stakes About' multiple bet is available in Betslip
        EXPECTED: 'Single Stakes About' multiple bet and 'Double Stakes About' multiple bet is available in Betslip
        """
        pass

    def test_002_verify_that_i_icon_is_displayed_next_to_single_stakes_about_multiple_bet_and_double_stakes_about_multiple_bet_is_available_in_betslip(self):
        """
        DESCRIPTION: Verify that 'i' icon is displayed next to 'Single Stakes About' multiple bet and 'Double Stakes About' multiple bet is available in Betslip
        EXPECTED: The 'i' icon is displayed next to the 'Single Stakes About' multiple bet and 'Double Stakes About' multiple bet is available in Betslip
        """
        pass

    def test_003_tap_on_i_icon_next_to_single_stakes_about_multiple_bet__and_verify_that_it_is_tappable(self):
        """
        DESCRIPTION: Tap on 'i' icon next to 'Single Stakes About' multiple bet  and verify that it is tappable
        EXPECTED: - The 'i' icon is tappable
        EXPECTED: - The pop up is displayed
        """
        pass

    def test_004_verify_pop_up_content(self):
        """
        DESCRIPTION: Verify pop up content
        EXPECTED: 'Single Stakes About' pop up message:
        EXPECTED: 'This bet consists of 2 single bets on two selections, the stake on each successful selection is re-invested on the other selection'.
        """
        pass

    def test_005_tap_on_i_icon_next_to_double_stakes_about_multiple_bet__and_verify_that_it_is_tappable(self):
        """
        DESCRIPTION: Tap on 'i' icon next to 'Double Stakes About' multiple bet  and verify that it is tappable
        EXPECTED: - The 'i' icon is tappable
        EXPECTED: - The pop up is displayed
        """
        pass

    def test_006_verify_pop_up_content(self):
        """
        DESCRIPTION: Verify pop up content
        EXPECTED: 'Double Stakes About' pop up message:
        EXPECTED: 'Like Single Stakes About, but where returns from the 1st winning selection are invested at double the original stake on the 2nd selection.'
        """
        pass

    def test_007_verify_that_the_popup_is_closable_via_ok_button(self):
        """
        DESCRIPTION: Verify that the popup is closable via OK button
        EXPECTED: The popup is closable via OK button
        """
        pass
