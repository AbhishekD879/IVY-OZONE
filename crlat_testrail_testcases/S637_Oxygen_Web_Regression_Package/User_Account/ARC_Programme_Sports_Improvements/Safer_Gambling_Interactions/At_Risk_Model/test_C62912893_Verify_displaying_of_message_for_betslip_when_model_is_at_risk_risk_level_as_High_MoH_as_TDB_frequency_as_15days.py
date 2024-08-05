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
class Test_C62912893_Verify_displaying_of_message_for_betslip_when_model_is_at_risk_risk_level_as_High_MoH_as_TDB_frequency_as_15days(Common):
    """
    TR_ID: C62912893
    NAME: Verify displaying of message for betslip when model is 'at risk' risk level as High& MoH as TDB & frequency as 15days
    DESCRIPTION: This test case verifies betslip when model as PG and risk level as High
    PRECONDITIONS: User Risk level should be High
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

    def test_003_in_cms_populate_all_fields_with_valid_data_model_at_riskrisk_level_lowmoh_tbd_and_frequency__15_days(self):
        """
        DESCRIPTION: In CMS populate all fields with valid data (Model-at risk,Risk Level-Low,MoH TBD and Frequency -15 days)
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
