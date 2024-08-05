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
class Test_C62912856_Verify_that_CMS_admin_user_can_edit_the_module_risk_fieldMoHProfileSport_action_Frequency_messaging_and_do_save_changes(Common):
    """
    TR_ID: C62912856
    NAME: Verify that CMS admin user can edit the module , risk field,MoH,Profile,Sport action ,Frequency & messaging and do save changes
    DESCRIPTION: This test case verifies the CMS user can do chnges and save
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

    def test_003_click_on_add_profile_and_enter_modelrisk_levelreason_codeprofile_auto_generated_sport_action_freauencyenable_check_box_and_click_on_save(self):
        """
        DESCRIPTION: Click on Add Profile and enter Modelrisk level,reason code,profile auto generated ,Sport action ,Freauency,enable check box and click on save
        EXPECTED: Profile should be saved with all the data entered
        """
        pass

    def test_004_click_on_edit_profile(self):
        """
        DESCRIPTION: Click on Edit profile
        EXPECTED: Profiles should be edited we can remove/Edit
        """
        pass

    def test_005_verify_model_risk_levelreason_codeprofile(self):
        """
        DESCRIPTION: Verify Model risk level,Reason code,Profile
        EXPECTED: All the mention fields should be in disable mode
        """
        pass

    def test_006_user_can_edit_sport_values(self):
        """
        DESCRIPTION: User can edit sport values
        EXPECTED: Multiple checkbox option available for user to select places where action needs to be activated.
        """
        pass

    def test_007_user_can_change_the_frequency(self):
        """
        DESCRIPTION: User can change the frequency
        EXPECTED: Frequency should be changed in CMS
        """
        pass

    def test_008_click_on_save_changes_in_cmsagain_click_on_save_changes(self):
        """
        DESCRIPTION: Click on save changes in CMS
        DESCRIPTION: Again click on save changes
        EXPECTED: All edited data  should be saved
        """
        pass

    def test_009_navigate_to_oxygen_application(self):
        """
        DESCRIPTION: Navigate to Oxygen application
        EXPECTED: 
        """
        pass

    def test_010_login_with_the_configured_arc_profile_user(self):
        """
        DESCRIPTION: Login with the configured ARC profile user
        EXPECTED: Login should be successful with the user and check the profile
        """
        pass
