import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2461987_Valid_for_OX98_Banach_Betslip_trigger_after_Reuse_selection_path_was_chosen(Common):
    """
    TR_ID: C2461987
    NAME: [Valid for OX98]  Banach. Betslip trigger after Reuse selection path was chosen
    DESCRIPTION: Test case verifies Betslip trigger after Reuse Selection option was selected
    DESCRIPTION: NOTE: 'Reuse selection' button seems to be removed in OX100 redesign
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check odds: open Dev tools > Network > **price** request
    PRECONDITIONS: **User has tapped Reuse Selection after Banach bet placement and sees selections dashboard**
    """
    keep_browser_open = True

    def test_001_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on Place bet button
        EXPECTED: Betslip is displayed with correct info:
        EXPECTED: - Title Betslip
        EXPECTED: - Selections names are the same as they were on dashboard
        EXPECTED: - Stake box
        EXPECTED: - Quick stakes
        EXPECTED: - Total Stake and Estimated Returns have value 0.00
        EXPECTED: - Back button
        EXPECTED: - Disabled Place bet button
        """
        pass

    def test_002_enter_a_stake_in_a_stake_box(self):
        """
        DESCRIPTION: Enter a stake in a stake box
        EXPECTED: - Total Stake and Estimated Returned are populated with the values
        EXPECTED: Total Stake - amount entered by user
        EXPECTED: Estimated Returns - calculated based on Odds value: (odds + 1)*stake
        EXPECTED: - PLACE BET button is enabled
        """
        pass
