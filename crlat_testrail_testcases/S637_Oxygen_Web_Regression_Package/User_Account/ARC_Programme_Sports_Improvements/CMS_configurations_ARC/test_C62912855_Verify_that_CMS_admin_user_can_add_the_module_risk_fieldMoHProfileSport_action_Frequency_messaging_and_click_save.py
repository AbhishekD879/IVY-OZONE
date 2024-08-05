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
class Test_C62912855_Verify_that_CMS_admin_user_can_add_the_module_risk_fieldMoHProfileSport_action_Frequency_messaging_and_click_save(Common):
    """
    TR_ID: C62912855
    NAME: Verify that CMS admin user can add the module , risk field,MoH,Profile,Sport action ,Frequency & messaging and click save
    DESCRIPTION: This test case verifies the CMS user can select all the fields and save
    PRECONDITIONS: User have CMS admin access
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: Login Should be successful
        """
        pass

    def test_002_navigate_to_arc_creation_screen(self):
        """
        DESCRIPTION: Navigate to ARC creation screen
        EXPECTED: ARC creation screen should be available
        """
        pass

    def test_003_click_on_add_profileadd_model_and_risk_level(self):
        """
        DESCRIPTION: Click on Add Profile
        DESCRIPTION: Add Model and Risk level
        EXPECTED: Drop down field with all the Model and risk levels
        """
        pass

    def test_004_user_can_select_reason_code_form_drop_down(self):
        """
        DESCRIPTION: User can select reason code form drop down
        EXPECTED: Drop down field with all relevant reason codes values
        """
        pass

    def test_005_user_can_select_profile_values(self):
        """
        DESCRIPTION: User can select profile values
        EXPECTED: Profile will be a auto generated based on the Model risk level and reason code
        """
        pass

    def test_006_user_can_select_sport_values(self):
        """
        DESCRIPTION: User can select sport values
        EXPECTED: Multiple checkbox option available for user to select places where action needs to be activated.Add message if required
        """
        pass

    def test_007_user_can_add_the_frequency(self):
        """
        DESCRIPTION: User can add the frequency
        EXPECTED: Frequency should be a number with increment and decrement indicator should be added in CMS
        """
        pass

    def test_008_click_on_enable_profileclick_on_green_tick(self):
        """
        DESCRIPTION: Click on Enable profile
        DESCRIPTION: Click on Green tick
        EXPECTED: Profile should be saved
        """
        pass

    def test_009_click_on_save_changes__in_cms(self):
        """
        DESCRIPTION: Click on save changes  in CMS
        EXPECTED: All entered profile data should be saved
        """
        pass
