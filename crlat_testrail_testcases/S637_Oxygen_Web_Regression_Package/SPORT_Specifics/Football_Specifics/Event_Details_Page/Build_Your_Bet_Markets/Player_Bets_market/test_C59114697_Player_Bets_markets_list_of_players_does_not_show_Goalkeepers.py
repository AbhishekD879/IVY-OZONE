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
class Test_C59114697_Player_Bets_markets_list_of_players_does_not_show_Goalkeepers(Common):
    """
    TR_ID: C59114697
    NAME: 'Player Bets' market's list of players does not show Goalkeepers
    DESCRIPTION: This test case verifies that Goalkeepers are not listed in the 'Player Bets' market
    PRECONDITIONS: Event with BYB mapping is available
    """
    keep_browser_open = True

    def test_001___navigate_to_the_event_details_page_where_build_your_betcoralbet_builderladbrokes_tab_is_available__open_byb_tab(self):
        """
        DESCRIPTION: - Navigate to the Event Details page where 'Build Your Bet'(Coral)/'Bet Builder'(Ladbrokes) tab is available
        DESCRIPTION: - Open BYB tab
        EXPECTED: BYB tab is opened, Player Bets market is present
        """
        pass

    def test_002___open_devtools_find_xhr_request_to_apiv1playersexample_httpsbuildyourbet_tst0coralcoukapiv1playersobeventid10294369__right_click_in_preview_tab_store_as_global_variable(self):
        """
        DESCRIPTION: - Open DevTools, find XHR request to /api/v1/players
        DESCRIPTION: (example: https://buildyourbet-tst0.coral.co.uk/api/v1/players?obEventId=10294369)
        DESCRIPTION: - Right click in Preview tab, Store as global variable
        EXPECTED: response is saved and shown as temp1 variable in console
        EXPECTED: ![](index.php?/attachments/get/113441616)
        """
        pass

    def test_003___execute_following_expression_in_console_to_get_list_of_goalkeeperstemp1datafilterplayer__playerpositiontitle__goalkeeper__verify_that_goalkeepers_are_not_present_in_select_a_player_dropdown_in_player_bets_marketor__check_response_manually_and_verify_that_players_who_has__positiontitle_goalkeeper__are_not_shown_in_player_bets_market(self):
        """
        DESCRIPTION: - execute following expression in console to get list of Goalkeepers:
        DESCRIPTION: temp1.data.filter(player => player.position.title === 'Goalkeeper')
        DESCRIPTION: - verify that Goalkeepers are NOT present in 'SELECT A PLAYER' dropdown in 'Player Bets' market
        DESCRIPTION: OR
        DESCRIPTION: - check response manually and verify that Players who has _position.title: "Goalkeeper"_ are not shown in 'Player Bets' market
        EXPECTED: Goalkeepers are not available for selection in 'Player Bets' market
        EXPECTED: ![](index.php?/attachments/get/113441666)
        """
        pass
