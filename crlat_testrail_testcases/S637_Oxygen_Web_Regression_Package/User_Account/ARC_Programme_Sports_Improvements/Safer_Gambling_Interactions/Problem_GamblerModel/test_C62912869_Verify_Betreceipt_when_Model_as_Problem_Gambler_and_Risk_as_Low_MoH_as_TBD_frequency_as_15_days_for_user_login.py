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
class Test_C62912869_Verify_Betreceipt_when_Model_as_Problem_Gambler_and_Risk_as_Low_MoH_as_TBD_frequency_as_15_days_for_user_login(Common):
    """
    TR_ID: C62912869
    NAME: Verify Betreceipt when Model as Problem Gambler and Risk as Low ,MoH as TBD &frequency as 15 days for  user login
    DESCRIPTION: This test case verifies Betreceipt when model as PG and risk level as low
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

    def test_003_in_cms_populate_all_fields_with_valid_data_model_problem_gamblerrisk_level_lowmoh_tbd_and_frequency_15_days_(self):
        """
        DESCRIPTION: In CMS populate all fields with valid data (Model-Problem Gambler,Risk Level-Low,MoH TBD and Frequency-15 days )
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
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_009_verify_bet_receipt_displaying_message_component(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying message component
        EXPECTED: Messaging component is displayed after bet placement as per CMS config
        """
        pass
