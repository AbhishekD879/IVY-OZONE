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
class Test_C59550817_Verify_that_Bets_are_not_duplicated_during_bet_placement_with_Overask(Common):
    """
    TR_ID: C59550817
    NAME: Verify that Bets are not duplicated during bet placement with Overask
    DESCRIPTION: This test case verifies that Bets are not duplicated during bet placement via Overask after selection change in Betslip
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in to the app
    PRECONDITIONS: 3. Overask functionality is enabled for the user
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Overask guides:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    """
    keep_browser_open = True

    def test_001__add_any_selection_from_eg_football_to_betslip_open_betslip(self):
        """
        DESCRIPTION: * Add any selection from e.g. Football to Betslip
        DESCRIPTION: * Open Betslip
        EXPECTED: Selection is present in Betslip
        """
        pass

    def test_002_trigger_price_change_for_the_selection_inside_betslip(self):
        """
        DESCRIPTION: Trigger price change for the selection inside Betslip
        EXPECTED: Price change message is displayed in Betslip
        """
        pass

    def test_003_remove_selection_from_betslip(self):
        """
        DESCRIPTION: Remove selection from Betslip
        EXPECTED: Betslip becomes empty and closes automatically
        """
        pass

    def test_004__add_anothersame_selection_from_eg_football_to_quickbet(self):
        """
        DESCRIPTION: * Add another/same selection from e.g. Football to Quickbet
        EXPECTED: Selection is present in Quickbet
        """
        pass

    def test_005__enter_a_stake_which_could_trigger_overask_bet_interception_tappress_place_bet_button(self):
        """
        DESCRIPTION: * Enter a stake which could trigger Overask Bet Interception
        DESCRIPTION: * Tap/Press 'Place bet' button
        EXPECTED: Betslip opens with Overask overlay is displayed
        """
        pass

    def test_006_open_related_tinavigate_to_bet__bi_requests__results_tab(self):
        """
        DESCRIPTION: Open related TI
        DESCRIPTION: Navigate to Bet > BI Requests > 'Results' tab
        EXPECTED: Only one request from the user is present in the list
        """
        pass

    def test_007__accept_the_bet_by_trader_observe_result_in_app(self):
        """
        DESCRIPTION: * Accept the bet by trader
        DESCRIPTION: * Observe result in app
        EXPECTED: Bet receipt is displayed with correct bet information
        """
        pass

    def test_008_navigate_to_my_bets__open_bets(self):
        """
        DESCRIPTION: Navigate to My Bets > Open Bets
        EXPECTED: Only one new bet from the user is present
        """
        pass
