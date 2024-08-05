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
class Test_C2983099_Verify_displaying_odds_boost_unavailable_popup_for_single_LP_selections_in_Betslip_Ineligible_Selection(Common):
    """
    TR_ID: C2983099
    NAME: Verify displaying odds boost unavailable popup for single LP selections in Betslip (Ineligible Selection)
    DESCRIPTION: 
    PRECONDITIONS: Create Odds Boost tokens with different Bet type using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: 1. Assign a token for a single bets and for specific league/type
    PRECONDITIONS: 2. Assign a token for a double bet and for a specific league/type
    PRECONDITIONS: 3. Login as a user with the tokens above assigned
    PRECONDITIONS: 4. Add an eligible single selection to the betslip
    PRECONDITIONS: 5. Add an eligible double selection to the betslip
    PRECONDITIONS: 6. Add some ineligible selections (ineligible selections - selection for which odds boost token cannot be applied)
    """
    keep_browser_open = True

    def test_001_open_the_betslip(self):
        """
        DESCRIPTION: Open the Betslip.
        EXPECTED: - Eligible and non-eligible selections are shown as not boosted.
        EXPECTED: - (i) icons are not shown for any of the selections.
        """
        pass

    def test_002_tap_boost_button_verify_ineligible_single_selections_displaying_in_the_betslip(self):
        """
        DESCRIPTION: Tap 'Boost' button. Verify ineligible single selections displaying in the Betslip.
        EXPECTED: * Odds remain unchanged for ineligible selections
        EXPECTED: * (i) icon appears in the left of the odds
        """
        pass

    def test_003_tap_i_icon(self):
        """
        DESCRIPTION: Tap (i) icon
        EXPECTED: Tooltip is shown with text: "Odds Boost is unavailable for this selection"
        """
        pass

    def test_004_tap_outside_the_tooltip(self):
        """
        DESCRIPTION: Tap outside the tooltip
        EXPECTED: Tooltip is closed
        """
        pass

    def test_005_verify_that_i_icon_isnt_added_to_the_boosted_single_and_multiple_selections(self):
        """
        DESCRIPTION: Verify that (i) icon isn't added to the boosted single and multiple selections
        EXPECTED: (i) icon is not shown for the boosted selections
        """
        pass

    def test_006_verify_the_i_icon_isnt_added_to_the_not_boosted_multiple_selection(self):
        """
        DESCRIPTION: Verify the (i) icon isn't added to the not-boosted multiple selection
        EXPECTED: (i) icon is not shown for the multiple selections even if they are not eligible
        """
        pass

    def test_007_tap_boosted_button_to_disable_odds_boost_verify_i_icon_disappears(self):
        """
        DESCRIPTION: Tap 'Boosted' button to disable Odds Boost. Verify (i) icon disappears.
        EXPECTED: - All odds get not boosted
        EXPECTED: - (i) icon for the ineligible single selections is not displayed anymore
        """
        pass
