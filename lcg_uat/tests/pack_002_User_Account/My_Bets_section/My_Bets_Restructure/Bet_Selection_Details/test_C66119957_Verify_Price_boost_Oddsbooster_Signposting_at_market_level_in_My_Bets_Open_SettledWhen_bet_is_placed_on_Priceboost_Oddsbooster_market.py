import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66119957_Verify_Price_boost_Oddsbooster_Signposting_at_market_level_in_My_Bets_Open_SettledWhen_bet_is_placed_on_Priceboost_Oddsbooster_market(
    Common):
    """
    TR_ID: C66119957
    NAME: Verify Price boost/Oddsbooster Signposting at market level in My Bets (Open, Settled)When bet is placed on Priceboost/Oddsbooster market
    DESCRIPTION: Verify Price boost/Oddsbooster Signposting at market level in My Bets (Open,Settled)When bet is placed on Priceboost/Oddsbooster market
    PRECONDITIONS: Priceboost/Oddsbooster maket slections should be available.
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_priceboostoddsbooster_market_selections_to_betslip_and_place_betladbrokes_priceboostcoral_odssbooster(
            self):
        """
        DESCRIPTION: Add priceboost/Oddsbooster market selections to betslip and place bet
        DESCRIPTION: Ladbrokes-Priceboost
        DESCRIPTION: Coral-Odssbooster
        EXPECTED: Bet placed successfully
        """
        pass
    
    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_004_verify_priceboostoddsbooster_signposting_at_market_level_in_open_tab_for_the_recently_placed_bet(self):
        """
        DESCRIPTION: Verify priceboost/oddsbooster signposting at market level in open tab for the recently placed bet
        EXPECTED: Priceboost/Odssbooster signposting should be displayed at market level.
        EXPECTED: It should horizontally aligned with market name.
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/cda8d7d7-8b8f-4fff-a54d-0bccfd40c9cc)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/76d7365b-a56c-4f58-8ee8-05af90774c6d)
        """
        pass

    def test_005_verify_the_bet_in_settled_once_it_is_resulted(self):
        """
        DESCRIPTION: Verify the bet in settled once it is resulted
        EXPECTED: Priceboost/Odssbooster signposting should be displayed at market level.
        EXPECTED: It should horizontally aligned with market name.
        """
        pass
