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
class Test_C62912883_Verify_displaying_of_messaging_for_my_Bets_when_Model_as_Problem_Gambler_and_Risk_level_as_High_Very_High_frequency_as_Permanent_display(Common):
    """
    TR_ID: C62912883
    NAME: Verify displaying of messaging for my Bets when Model as Problem Gambler and Risk level as High, Very High & frequency as Permanent display
    DESCRIPTION: This test case verifies my bets when model as PG and risk level as High,Very High
    PRECONDITIONS: .User Risk level should be High, Very High
    PRECONDITIONS: Frequency should be set in CMS
    PRECONDITIONS: .Messaging component displayed as per CMS
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

    def test_003_in_cms_populate_all_fields_with_valid_data_model_problem_gamblerrisk_level_highmoh_tbd_and_frequency_permanent__(self):
        """
        DESCRIPTION: In CMS populate all fields with valid data (Model-Problem Gambler,Risk Level-High,MoH TBD and Frequency-permanent  )
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

    def test_007_verify_bet_receipt_displaying_message_component_after_clickingtapping_the_place_bet_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying message component after clicking/tapping the 'Place Bet' button
        EXPECTED: Messaging component is displayed after bet placement as per CMS config
        """
        pass

    def test_008_add_several__selection_to_betslip_and_place_and_doubletripleacca_etc_and_tab_on_place_bet_button(self):
        """
        DESCRIPTION: Add several  selection to betslip and place and double,triple,Acca etc and tab on place bet button
        EXPECTED: .Bet is placed successfully
        EXPECTED: .Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_009_navigate_to_my_bets__open_bets_tab(self):
        """
        DESCRIPTION: Navigate to My bets- Open Bets tab
        EXPECTED: Placed bets is displayed ,Messaging component is displayed after bet placement as per CMS
        """
        pass

    def test_010_when_user_click_on_message_link(self):
        """
        DESCRIPTION: When user click on message link
        EXPECTED: Application will re-direct user to Bet limit setting screen
        """
        pass

    def test_011_repeat_the_same_for_multiplecomplex_bets__and_place_the_bets(self):
        """
        DESCRIPTION: Repeat the same for multiple,complex bets  and place the bets
        EXPECTED: .Bet is placed successfully
        EXPECTED: .Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_012_navigate_to_my_bets__open_bets_tab(self):
        """
        DESCRIPTION: Navigate to My bets- Open Bets tab
        EXPECTED: Placed bets is displayed ,Messaging component is displayed after bet placement as per CMS
        """
        pass

    def test_013_when_user_click_on_message_link(self):
        """
        DESCRIPTION: When user click on message link
        EXPECTED: Application will re-direct user Bet limit setting screen
        """
        pass

    def test_014_repeat_the_above_steps_for_risk_level_as_very_high_moh_tbd_and_frequency_permanent__(self):
        """
        DESCRIPTION: Repeat the above steps for Risk level as very high ,MoH TBD and Frequency-permanent  )
        EXPECTED: Messaging component is displayed after bet placement as per CMS config
        """
        pass
