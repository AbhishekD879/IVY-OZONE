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
class Test_C29038_Multiples_Details(Common):
    """
    TR_ID: C29038
    NAME: Multiples Details
    DESCRIPTION: This test case verifies information displayed on Multiples page
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_several_selections_from_different_events_to_thebetslip(self):
        """
        DESCRIPTION: Add several selections from different events to the betslip
        EXPECTED: 
        """
        pass

    def test_002_open_betslip_and_scroll_to_multiples_section(self):
        """
        DESCRIPTION: Open Betslip and scroll to 'Multiples' section
        EXPECTED: Multiples are available for added selections.
        EXPECTED: Section title is "Multiples (#)"
        EXPECTED: where # is number of available Multiple Types
        """
        pass

    def test_003_verify_number_of_multiples(self):
        """
        DESCRIPTION: Verify number of Multiples
        EXPECTED: The number of available Multiples is displayed near section title in brackets and corresponds to the number of Multiples displayed on the page below
        """
        pass

    def test_004_verify_information_icon(self):
        """
        DESCRIPTION: Verify 'Information' icon
        EXPECTED: 'Information' icon should be available for each of the Multiple bet type that is formed in the Multiples section of the Betslip
        EXPECTED: When the Icon is clicked a popup with informative text, which describes this type of the bet, should appear
        """
        pass

    def test_005_verify_multiple_bet_type_name(self):
        """
        DESCRIPTION: Verify Multiple Bet Type name
        EXPECTED: Multiple Bet Type name should be displayed next to the 'Information' icon
        """
        pass

    def test_006_verify_number_of_bets_for_multiple_type(self):
        """
        DESCRIPTION: Verify Number of Bets for Multiple Type
        EXPECTED: Number of Bets should be displayed next to the Multiple bet type name and should display the number of bets involved in a Multiple. Value it taken from server
        """
        pass

    def test_007_verify_stake_field(self):
        """
        DESCRIPTION: Verify 'Stake' field
        EXPECTED: 'Stake' field to enter the amount, titled 'Stake', should be present right below each Multiple bet type
        EXPECTED: Default value is £0.00 (currency symbol corresponds to user's currency)
        """
        pass

    def test_008_verify_est_returns(self):
        """
        DESCRIPTION: Verify 'Est. Returns'
        EXPECTED: 'Est. Returns' field is available for each Multiple Type
        EXPECTED: Default value is £0.00  (currency symbol corresponds to user's currency) or N/A (in case selection with SP price was added)
        """
        pass

    def test_009_enter_stake_for_multiple(self):
        """
        DESCRIPTION: Enter 'Stake' for Multiple
        EXPECTED: 'Est. Returns' field is calculated for this Multiple bet
        """
        pass
