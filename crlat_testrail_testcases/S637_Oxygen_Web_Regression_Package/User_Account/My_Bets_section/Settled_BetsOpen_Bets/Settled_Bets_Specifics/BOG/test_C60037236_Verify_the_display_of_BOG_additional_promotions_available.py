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
class Test_C60037236_Verify_the_display_of_BOG_additional_promotions_available(Common):
    """
    TR_ID: C60037236
    NAME: Verify the display of BOG -additional promotions available
    DESCRIPTION: This test case verify BOG text and price difference in Settled bet tab when the events have BOG signpost and BOG flag is ON in CMS and also additional signposting (Extra Place, Cashout etc)
    PRECONDITIONS: 1. BOG has been enabled in CMS(Sysytem config)
    PRECONDITIONS: 2. BOG Signposting, Pop-up configured with Header, Pop-up text and Link in CMS (CMS > Promotions > Promotions)
    PRECONDITIONS: 3. Events with market configured to show BOG flag available (Market should have 'GP Available' 'SP Available' and 'LP Available' checkmarks)
    PRECONDITIONS: 4. Extra place/ Cashout signposting should be enabled
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: Ladbrokes/Coral URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        pass

    def test_003_click_on_any_horse_race_event_which_has_extra_place_cashout_signpost_along_with_bog(self):
        """
        DESCRIPTION: Click on any Horse race event which has extra place /cashout signpost along with BOG
        EXPECTED: User should be navigated to EDP
        """
        pass

    def test_004_add_a_hr_selectionselections_to_bet_slip(self):
        """
        DESCRIPTION: Add a HR selection/selections to bet slip
        EXPECTED: The selection/selections is added to bet slip
        """
        pass

    def test_005_enter_the_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Enter the Stake and click on Place bet button
        EXPECTED: User should be able to place the bet successfully
        EXPECTED: Bet receipt should be generated
        EXPECTED: Wait till event is settled
        """
        pass

    def test_006_navigate_to_settled_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page
        EXPECTED: Bet History' page/tab is opened
        """
        pass

    def test_007_verify_the_bog_text_and_price_differencesindexphpattachmentsget131712256(self):
        """
        DESCRIPTION: Verify the BOG text and Price differences![](index.php?/attachments/get/131712256)
        EXPECTED: * BOG Best Odds Guaranteed should be displayed above Event time & Name
        EXPECTED: * You won £xx.xx extra with BOG offer should be displayed above the Stake and Returns
        EXPECTED: £xx.xx- Price difference
        EXPECTED: * Bet Receipt should be displayed below and Time & Date on right side
        EXPECTED: Note: If BOG is applicable ,the potential Returns includes the Extra Winnings.
        """
        pass
