import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.
@vtest
class Test_C59486936_Verify_the_order_of_Cashout_Extraplace_and_BOG_signposting_displayed_in_HR_Result_tab(Common):
    """
    TR_ID: C59486936
    NAME: Verify the order of Cashout, Extraplace and  BOG signposting displayed in HR Result tab
    DESCRIPTION: This test case verify BOG text and price difference in Settled bet tab when the events have BOG signpost and BOG flag is ON in CMS
    PRECONDITIONS: 1. BOG has been enabled in CMS(Sysytem config)
    PRECONDITIONS: 2. BOG Signposting, Pop-up configured with Header, Pop-up text and Link in CMS (CMS > Promotions > Promotions)
    PRECONDITIONS: 3. Events with market configured to show BOG flag available (Market should have 'GP Available' 'SP Available' and 'LP Available' checkmarks)
    PRECONDITIONS: 4. Extra place signposting should be enabled
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

    def test_003_click_on_any_horse_race_event_which_has_cash_out_and_bog_placeextra_place_signpost(self):
        """
        DESCRIPTION: Click on any Horse race event which has cash out and BOG place,Extra place signpost
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

    def test_007_verify_the_bog_signposting_order(self):
        """
        DESCRIPTION: Verify the BOG signposting order
        EXPECTED: It should be on the right hand side of the two .
        """
        pass
