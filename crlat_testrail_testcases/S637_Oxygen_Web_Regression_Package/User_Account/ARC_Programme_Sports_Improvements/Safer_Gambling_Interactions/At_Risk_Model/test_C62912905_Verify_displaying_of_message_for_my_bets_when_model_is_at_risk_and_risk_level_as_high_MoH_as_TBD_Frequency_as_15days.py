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
class Test_C62912905_Verify_displaying_of_message_for_my_bets_when_model_is_at_risk_and_risk_level_as_high_MoH_as_TBD_Frequency_as_15days(Common):
    """
    TR_ID: C62912905
    NAME: Verify displaying of message for my bets when model is 'at risk' and risk level as high & MoH as TBD & Frequency as 15days
    DESCRIPTION: This test case verifies messaging component in  my bets when model At Risk and Risk as High & MoH as TBD & frequency as 15 days
    PRECONDITIONS: User Risk level should be Low
    PRECONDITIONS: Frequency should be set in CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: Login should be successful
        """
        pass

    def test_002_navigate_to_arc_creation_screen(self):
        """
        DESCRIPTION: Navigate to ARC creation screen
        EXPECTED: ARC creation screen should be available
        """
        pass

    def test_003_in_cms_populate_all_fields_with_valid_data_model_problem_gamblerrisk_level_highmoh_tbd_and_frequency_15_days_(self):
        """
        DESCRIPTION: In CMS populate all fields with valid data (Model-Problem Gambler,Risk Level-High,MoH TBD and Frequency-15 days )
        EXPECTED: Data should be saved
        """
        pass

    def test_004_login_to_application(self):
        """
        DESCRIPTION: Login to Application
        EXPECTED: User should login successfully
        """
        pass

    def test_005_application__identifies_the_user_category_based_on_demographics_details(self):
        """
        DESCRIPTION: Application  identifies the user category based on demographics details
        EXPECTED: Details as per CMS
        """
        pass

    def test_006_go_to_any_sport_and_add_single_selection_to_betslip(self):
        """
        DESCRIPTION: Go to any sport and add single selection to betslip
        EXPECTED: Selection is displayed and  added to betslip
        """
        pass

    def test_007_verify_bet_receipt_displaying_after_clickingtapping_the_place_bet_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Place Bet' button
        EXPECTED: .Bet is placed successfully
        EXPECTED: .Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_008_navigate_to_my_bets__open_bets_tab(self):
        """
        DESCRIPTION: Navigate to My bets- Open Bets tab
        EXPECTED: Placed bets is displayed ,Messaging component is displayed after bet placement as per CMS
        """
        pass

    def test_009_when_user_click_on_message_link(self):
        """
        DESCRIPTION: When user click on message link
        EXPECTED: Application will re-direct user to RG screen
        """
        pass

    def test_010_repeat_the_same_for_multiplecomplex_bets__and_place_the_bets(self):
        """
        DESCRIPTION: Repeat the same for multiple,complex bets  and place the bets
        EXPECTED: .Bet is placed successfully
        EXPECTED: .Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_011_navigate_to_my_bets__open_bets_tab(self):
        """
        DESCRIPTION: Navigate to My bets- Open Bets tab
        EXPECTED: Placed bets is displayed ,Messaging component is displayed after bet placement as per CMS
        """
        pass

    def test_012_when_user_click_on_message_link(self):
        """
        DESCRIPTION: When user click on message link
        EXPECTED: Application will re-direct user to RG screen
        """
        pass
