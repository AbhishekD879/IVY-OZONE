import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C51875589_Vanilla_Ladbrokes_Verify_Tooltip_pop_up_for_Free_Bets_on_invalid_Bet_Levels(Common):
    """
    TR_ID: C51875589
    NAME: [Vanilla Ladbrokes] Verify Tooltip pop up for Free Bets on invalid Bet Level(s)
    DESCRIPTION: This test case verifies FreeBet "i" (information) icon pop up for Free Bets with Redemption values on unavailable Bet Level
    PRECONDITIONS: - User has FreeBet(s) available with next 'Single/Multiple Redemption Values' on any 'Category'/'Class'/'Type'/'Event'/'Market'/'Selection' Bet Levels
    PRECONDITIONS: - 'Category'/'Class'/'Type'/'Event'/'Market'/'Selection' from Step 1 are undisplayed in OB
    PRECONDITIONS: - Instruction how to create a 'Redemption Value' & add a Free Bet to a user: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Event
    """
    keep_browser_open = True

    def test_001_navigate_to_my_account_menu__offers__sports_free_bets(self):
        """
        DESCRIPTION: Navigate to My Account menu > Offers > Sports Free Bets
        EXPECTED: Sports Free Bets Page is opened
        """
        pass

    def test_002_tap_on_i_information_icon_of_a_free_bet_that_applies_on_a_single_or_multiple_bet_levelsfrom_preconditions_1__2(self):
        """
        DESCRIPTION: Tap on "i" (information) icon of a Free Bet that applies on a single or multiple bet levels
        DESCRIPTION: (from Preconditions 1 & 2)
        EXPECTED: Pop up is displayed with text FreeBet:
        EXPECTED: "This Free Bet can be used for any event."
        """
        pass
