import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C51829459_Vanilla_Ladbrokes_Verify_Tooltip_pop_up_for_Free_Bets_on_Multiple_Bet_Levels(Common):
    """
    TR_ID: C51829459
    NAME: [Vanilla Ladbrokes] Verify Tooltip pop up for Free Bets on Multiple Bet Levels
    DESCRIPTION: This test case verifies FreeBet "i" (information) icon pop up for Free Bets with Multiple Redemption values
    PRECONDITIONS: - User has FreeBet(s) available with next 'Multiple Redemption Values' on 'Category', 'Class', 'Type', 'Event', 'Market', 'Selection' Bet Levels
    PRECONDITIONS: - Instruction how to create a 'Redemption Value' & add a Free Bet to a user: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Event
    PRECONDITIONS: - User with free bets is logged in an app
    """
    keep_browser_open = True

    def test_001_navigate_to_my_account_menu__offers__sports_free_bets(self):
        """
        DESCRIPTION: Navigate to My Account menu > Offers > Sports Free Bets
        EXPECTED: Sports Free Bets page is opened
        """
        pass

    def test_002_tap_on_i_information_icon_of_a_free_bet_that_applies_on_a_multiple_bet_levelsredemption_value__redemption_value_from_preconditions(self):
        """
        DESCRIPTION: Tap on "i" (information) icon of a Free Bet that applies on a multiple bet levels
        DESCRIPTION: ('Redemption Value' = redemption value from preconditions)
        EXPECTED: Pop up is displayed with text FreeBet:
        EXPECTED: "This Free Bet can be used for < 'Category' e.g. Football events, 'Class' e.g. Football England events, 'Type' e.g. Premier League events, 'Event' e.g. Chelsea vs Liverpool event>."
        """
        pass
