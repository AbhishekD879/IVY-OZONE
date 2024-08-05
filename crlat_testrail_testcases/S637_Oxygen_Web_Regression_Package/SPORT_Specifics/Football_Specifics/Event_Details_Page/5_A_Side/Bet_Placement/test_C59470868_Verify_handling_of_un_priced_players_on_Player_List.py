import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C59470868_Verify_handling_of_un_priced_players_on_Player_List(Common):
    """
    TR_ID: C59470868
    NAME: Verify handling of un-priced players on Player List
    DESCRIPTION: This TC verifies handling of Players when they don't have price for the selected market.
    PRECONDITIONS: 1. 5-A-Side event
    PRECONDITIONS: 2. User is navigated to 5-A-Side tab on EDP
    PRECONDITIONS: 3. DevTools Network tab is opened
    """
    keep_browser_open = True

    def test_001___click_build_team__click_plus_to_add_a_marketeg_assists(self):
        """
        DESCRIPTION: - Click 'BUILD TEAM'
        DESCRIPTION: - Click '+' to add a market(e.g. Assists)
        EXPECTED: Players List is shown
        """
        pass

    def test_002___select_a_player_who_doesnt_have_current_market_eg_try_to_add_any_goalkeeper_player_to_assists_marketnote_market_is_not_available_for_the_player_if_its_not_received_from_banach_in_apiv1player_statisticsplayerid_responseexample_of_url_httpsbuildyourbet_tst0ladbrokesoxygennonprodcloudladbrokescoralcomapiv1player_statisticsobeventid989737playerid10(self):
        """
        DESCRIPTION: - Select a player who doesn't have current market (e.g. try to add any 'Goalkeeper' player to 'Assists' market)
        DESCRIPTION: NOTE: Market is not available for the Player if it's not received from Banach in api/v1/player-statistics?playerId= response
        DESCRIPTION: example of URL https://buildyourbet-tst0.ladbrokesoxygen.nonprod.cloud.ladbrokescoral.com/api/v1/player-statistics?obEventId=989737&playerId=10
        EXPECTED: - Popup message is shown "Sorry, this player is unavailable for this betting market"
        EXPECTED: ![](index.php?/attachments/get/114764016)
        EXPECTED: - Player is greyed-out(but is still clickable) in Players list once popup is closed
        EXPECTED: ![](index.php?/attachments/get/114764018)
        """
        pass
