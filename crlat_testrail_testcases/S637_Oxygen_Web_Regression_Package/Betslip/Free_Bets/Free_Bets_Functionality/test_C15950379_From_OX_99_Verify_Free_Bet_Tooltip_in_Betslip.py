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
class Test_C15950379_From_OX_99_Verify_Free_Bet_Tooltip_in_Betslip(Common):
    """
    TR_ID: C15950379
    NAME: [From OX 99] Verify Free Bet Tooltip in Betslip
    DESCRIPTION: This test case verifies Free Bets tooltip in the Betslip
    DESCRIPTION: **FROM OX105 (BMA-52025) - tooltip is shown only once - steps should be updated**
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has Free Bets available on their account
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip and open Betslip
        EXPECTED: Betslip is open
        EXPECTED: Free Bet Tooltip is shown
        """
        pass

    def test_002_tap_on_any_part_of_the_betslip(self):
        """
        DESCRIPTION: Tap on any part of the Betslip
        EXPECTED: * Free Bet Tooltip is closed
        EXPECTED: * *OX.freeBetTooltipSeen-username* key (Local Storage) is set as true
        """
        pass

    def test_003_add_more_selections_to_the_betslip_and_open_it(self):
        """
        DESCRIPTION: Add more selections to the Betslip and open it
        EXPECTED: Free Bet Tooltip is NOT shown
        """
        pass

    def test_004_remove_all_selections_and_add_a_new_ones(self):
        """
        DESCRIPTION: Remove all selections and add a new one(s)
        EXPECTED: Free Bet Tooltip is NOT shown
        """
        pass

    def test_005_remove_all_selections_from_the_betslipremove_oxfreebettooltipseen_username_keyadd_selection_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Remove all selections from the Betslip
        DESCRIPTION: Remove *OX.freeBetTooltipSeen-username* key
        DESCRIPTION: Add selection to the Betslip and open Betslip
        EXPECTED: Betslip is open
        EXPECTED: Free Bet Tooltip is shown
        """
        pass

    def test_006_tap_on_any_part_of_the_betslip(self):
        """
        DESCRIPTION: Tap on any part of the Betslip
        EXPECTED: * Free Bet Tooltip is closed
        EXPECTED: * *OX.freeBetTooltipSeen-username* key (Local Storage) is set as true
        """
        pass
