import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870394_Verify_if_the_Cash_Out_value_is_calculated_correctly_and_Cash_Out_can_be_done_successfully_for_the_bet_placed_on_Player_Assists_Player_Tackles_market_published_from_Banach(Common):
    """
    TR_ID: C44870394
    NAME: Verify if the Cash Out value is calculated correctly and Cash Out can be done successfully for the bet placed on  Player Assists + Player Tackles market published from Banach
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_httpsmsportsladbrokescom(self):
        """
        DESCRIPTION: Open https://msports.ladbrokes.com
        EXPECTED: Ladbrokes application launched
        """
        pass

    def test_002_navigate_to_football(self):
        """
        DESCRIPTION: Navigate to Football
        EXPECTED: Football LP displayed
        """
        pass

    def test_003_select_football_event_which_contains_player_assists_plus_player_tackles_markets_and_place_bets(self):
        """
        DESCRIPTION: Select football event which contains Player Assists + Player Tackles markets and place bets
        EXPECTED: Bets placed successfully on player assists and player tackles market selections
        """
        pass

    def test_004_verify_cashout_value_in_my_bets_and_verify_correct_amount_is_received_when_cashing_out(self):
        """
        DESCRIPTION: Verify cashout value in my bets and verify correct amount is received when cashing out
        EXPECTED: Cashout value is correct and value cashed out is correct.
        """
        pass
