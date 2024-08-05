import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.
@vtest
class Test_C59486935_Verify_BOG_help_text_in_pop_up_when_click_on_BOG_signpost(Common):
    """
    TR_ID: C59486935
    NAME: Verify BOG help text in pop up when click on BOG signpost
    DESCRIPTION: This test case verify BOG help text in pop up when click on BOG signpost
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

    def test_003_click_on_any_horse_race_event_which_has_bog_place_signpost(self):
        """
        DESCRIPTION: Click on any Horse race event which has BOG place signpost
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
        EXPECTED: Wait till event is settled
        """
        pass

    def test_006_navigate_to_result_tab_on_horse_racing_edp__page(self):
        """
        DESCRIPTION: Navigate to 'Result' tab on Horse racing EDP ' page
        EXPECTED: Event Details page should be opened
        """
        pass

    def test_007_click_on_bog_sign_post(self):
        """
        DESCRIPTION: Click on BOG sign post
        EXPECTED: Pop up should be opened with the described text and Contains with  OK & More buttons
        EXPECTED: Text, navigation should be as per pre condition # 2
        """
        pass

    def test_008_click_on_ok_button(self):
        """
        DESCRIPTION: Click on OK button
        EXPECTED: pop up should be closed
        """
        pass

    def test_009_click_on_tcs_apply_button(self):
        """
        DESCRIPTION: Click on T&C's Apply button
        EXPECTED: Terms and conditions page should be open
        """
        pass
