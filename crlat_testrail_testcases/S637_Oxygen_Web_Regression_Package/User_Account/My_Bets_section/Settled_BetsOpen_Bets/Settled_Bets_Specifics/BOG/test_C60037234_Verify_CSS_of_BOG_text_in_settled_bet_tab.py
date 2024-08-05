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
class Test_C60037234_Verify_CSS_of_BOG_text_in_settled_bet_tab(Common):
    """
    TR_ID: C60037234
    NAME: Verify CSS of BOG text in settled bet tab
    DESCRIPTION: This test case Verify BOG text and price difference is not displayed in Settled bet tab when the BOG toggle is OFF in CMS
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

    def test_006_navigate_to_settled_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page
        EXPECTED: Bet History' page/tab is opened
        """
        pass

    def test_007_verify_the_css_for_bog(self):
        """
        DESCRIPTION: Verify the CSS for BOG
        EXPECTED: .Best-odds-Guaranteed {
        EXPECTED: width: 142px;
        EXPECTED: height: 16px;
        EXPECTED: margin: 15px 91px 1px 8px;
        EXPECTED: font-family: HelveticaNeue;
        EXPECTED: font-size: 14px;
        EXPECTED: font-weight: normal;
        EXPECTED: font-stretch: normal;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: 0px;
        EXPECTED: color: #2b2b2b;
        EXPECTED: }
        EXPECTED: .Rectangle-8-Copy-3 {
        EXPECTED: width: 367px;
        EXPECTED: height: 237px;
        EXPECTED: margin: 12px 4px 16px;
        EXPECTED: padding: 0 0 12px;
        EXPECTED: box-shadow: 0 -1px 2px 0 rgba(0, 0, 0, 0.05), 0 2px 4px 0 rgba(0, 0, 0, 0.15);
        EXPECTED: background-color: #ffffff;
        EXPECTED: }
        EXPECTED: .Best-odds-Guaranteed {
        EXPECTED: width: 129px;
        EXPECTED: height: 16px;
        EXPECTED: margin: 10px 132px 3px 10px;
        EXPECTED: font-family: Lato;
        EXPECTED: font-size: 13px;
        EXPECTED: font-weight: normal;
        EXPECTED: font-stretch: normal;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: normal;
        EXPECTED: color: #41494e;
        EXPECTED: }
        EXPECTED: .You-earned-1125 {
        EXPECTED: width: 96px;
        EXPECTED: height: 13px;
        EXPECTED: margin: 3px 165px 0 10px;
        EXPECTED: font-family: Lato;
        EXPECTED: font-size: 11px;
        EXPECTED: font-weight: bold;
        EXPECTED: font-stretch: normal;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: 0px;
        EXPECTED: color: #084d8d;
        EXPECTED: }
        """
        pass
