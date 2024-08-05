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
class Test_C58419484_Verify_that_Odds_Boost_is_unavailable_for_this_selection_error_message_is_shown_in_the_Betslip_after_tapping_on_i_icon(Common):
    """
    TR_ID: C58419484
    NAME: Verify that "Odds Boost is unavailable for this selection' error message is shown in the Betslip after tapping on 'i' icon"
    DESCRIPTION: This test case verifies that "Odds Boost is unavailable for this selection' error message is shown in the Betslip after tapping on 'i' icon"
    PRECONDITIONS: Load application and login with User with odds boost token ANY available
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token - instruction for generating tokens
    PRECONDITIONS: OpenBet Systems: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True

    def test_001_add_three_selections_to_the_betslip__add_selection_hr_with_sp_only_available_selection_1__add_selection_hr_with_lp_and_sp_available_selection_2_and_lp_price_is_selected__add_selection_hr_with_lp_and_sp_available_selection_3_and_lp_price_is_selected(self):
        """
        DESCRIPTION: Add three selections to the Betslip:
        DESCRIPTION: - Add selection (HR) with SP only available (Selection_1)
        DESCRIPTION: - Add selection (HR) with LP and SP available (Selection_2) and LP price is selected
        DESCRIPTION: - Add selection (HR) with LP and SP available (Selection_3) and LP price is selected
        EXPECTED: Selections are added
        """
        pass

    def test_002_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Selections are added and not boosted
        """
        pass

    def test_003_add_stake_for_the_selection_1_and_tap_a_boost_button(self):
        """
        DESCRIPTION: Add Stake for the Selection_1 and tap a 'BOOST' button
        EXPECTED: 'i' icon appears next to Selection_1
        """
        pass

    def test_004_tap_i_icon_for_selection_1(self):
        """
        DESCRIPTION: Tap 'i' icon for Selection_1
        EXPECTED: 'Odds Boost is unavailable for this selection' is shown in the Betslip after tapping on 'i' icon
        """
        pass
