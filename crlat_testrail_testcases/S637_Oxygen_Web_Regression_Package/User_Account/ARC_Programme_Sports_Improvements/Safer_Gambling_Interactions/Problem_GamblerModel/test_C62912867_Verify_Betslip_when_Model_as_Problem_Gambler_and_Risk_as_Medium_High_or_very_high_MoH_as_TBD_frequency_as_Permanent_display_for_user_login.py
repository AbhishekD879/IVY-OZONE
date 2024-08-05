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
class Test_C62912867_Verify_Betslip_when_Model_as_Problem_Gambler_and_Risk_as_Medium_High_or_very_high_MoH_as_TBD_frequency_as_Permanent_display_for_user_login(Common):
    """
    TR_ID: C62912867
    NAME: Verify Betslip when Model as Problem Gambler and Risk as Medium, High or very high & MoH as TBD & frequency as Permanent display for user login
    DESCRIPTION: This test case verifies betslip when model as PG and risk level as Medium,high&very high
    PRECONDITIONS: User Risk level should be medium, high &very high
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

    def test_003_in_cms_populate_all_fields_with_valid_data_model_problem_gamblerrisk_level_mediummoh_tbd_and_frequency_permanent_display_(self):
        """
        DESCRIPTION: In CMS populate all fields with valid data (Model-Problem Gambler,Risk Level-Medium,MoH TBD and Frequency Permanent display )
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

    def test_007_check_the_messaging_in_betslip(self):
        """
        DESCRIPTION: Check the Messaging in Betslip
        EXPECTED: Messaging component is displayed prior to bet placement as per CMS config
        """
        pass

    def test_008_add_several__selection_to_betslip(self):
        """
        DESCRIPTION: Add several  selection to betslip
        EXPECTED: Multiples are available for added selections
        """
        pass

    def test_009_check_the_messaging_in_betslip(self):
        """
        DESCRIPTION: Check the Messaging in Betslip
        EXPECTED: Messaging component is displayed prior to bet placement as per CMS config
        """
        pass

    def test_010_repeat_the_above_steps_for_risk_level_as_high__very_high(self):
        """
        DESCRIPTION: Repeat the above steps for Risk level as High & very high
        EXPECTED: Messaging component is displayed prior to bet placement as per CMS config
        """
        pass
