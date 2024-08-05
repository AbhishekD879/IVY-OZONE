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
class Test_C62912863_Verify_user_demographics_details_based_on_the_user_category_for_login(Common):
    """
    TR_ID: C62912863
    NAME: Verify user demographics details based on the user category for login
    DESCRIPTION: This test case verifies user demographics details based on the user category
    PRECONDITIONS: Changes in application should apply   (message display, user interaction) only on fresh session and not current session
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

    def test_003_in_cms_populate_all_fields_with_valid_data_modelrisk_levelmoh_type_and_user_profile(self):
        """
        DESCRIPTION: In CMS Populate all fields with valid data (Model,Risk Level,MoH type and user profile)
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

    def test_006_change_any_model_or_risk_level_and_save(self):
        """
        DESCRIPTION: Change any model or risk level and save
        EXPECTED: Changes should be saved
        """
        pass

    def test_007_application_should_apply_the_changes(self):
        """
        DESCRIPTION: Application should apply the changes
        EXPECTED: Changes should only on fresh session and not current session.
        """
        pass
