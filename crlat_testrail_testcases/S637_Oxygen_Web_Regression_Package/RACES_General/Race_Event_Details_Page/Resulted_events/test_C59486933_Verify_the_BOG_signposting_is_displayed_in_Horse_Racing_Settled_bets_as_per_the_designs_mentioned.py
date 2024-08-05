import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C59486933_Verify_the_BOG_signposting_is_displayed_in_Horse_Racing_Settled_bets_as_per_the_designs_mentioned(Common):
    """
    TR_ID: C59486933
    NAME: Verify the BOG signposting is displayed in Horse Racing "Settled bets" as per the designs mentioned
    DESCRIPTION: This test case Verify BOG text and price difference is displayed in Settled bet tab when the BOG toggle is ON in CMS
    PRECONDITIONS: 1. BOG has been enabled in CMS(Sysytem config)
    PRECONDITIONS: 2. BOG Signposting, Pop-up configured with Header, Pop-up text and Link in CMS (CMS > Promotions > Promotions)
    PRECONDITIONS: 3. Events with market configured to show BOG flag available (Market should have 'GP Available' 'SP Available' and 'LP Available' checkmarks)
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

    def test_003_click_on_any_horse_race_event_from_which_have_bog_signpost(self):
        """
        DESCRIPTION: Click on any Horse race event from which have BOG signpost
        EXPECTED: It should be displayed below on Horses in HR EDP
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
        """
        pass

    def test_006_navigate_to_settled_bets_tab_on_my_bets(self):
        """
        DESCRIPTION: Navigate to 'Settled bets' tab on My Bets
        EXPECTED: Settled Bets tab should be opened
        """
        pass

    def test_007_verify_the_bog_signposting(self):
        """
        DESCRIPTION: Verify the BOG signposting
        EXPECTED: BOG should be displayed as per the zeplin screen
        """
        pass
