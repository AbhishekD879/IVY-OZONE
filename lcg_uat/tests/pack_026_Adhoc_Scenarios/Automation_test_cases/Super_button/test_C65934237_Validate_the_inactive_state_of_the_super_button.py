import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65934237_Validate_the_inactive_state_of_the_super_button(Common):
    """
    TR_ID: C65934237
    NAME: Validate the inactive state of the super button.
    DESCRIPTION: This test case is to validate the inactive state of the super button. Super button should not be displayed in FE if it is in inactive state.
    PRECONDITIONS: Active Super button which is in running state should be available.
    """
    keep_browser_open = True

    def test_001_launch_the_oxygen_application(self):
        """
        DESCRIPTION: Launch the oxygen application.
        EXPECTED: Application should be loaded successfully home tab should be loaded by default.
        """
        pass

    def test_002_verify_configured_super_button_is_displaying_in_fe(self):
        """
        DESCRIPTION: Verify configured super button is displaying in FE
        EXPECTED: Super button should be displayed on homepage by default.
        """
        pass

    def test_003_now_go_to_cmsgthome_page_modulegtsuper_button_screen_and_click_on_configured_super_button_gtthen_uncheck_the_active_check_box_and_save_it(self):
        """
        DESCRIPTION: Now go to CMS&gt;Home page module&gt;Super button screen and click on configured super button &gt;then uncheck the Active check box and save it.
        EXPECTED: Changes should be saved successfully.
        """
        pass

    def test_004_navigate_to_fe_and_validate_super_button_is_displaying_or_not(self):
        """
        DESCRIPTION: Navigate to FE and validate super button is displaying or not.
        EXPECTED: Super button should not be displayed.
        """
        pass

    def test_005_login_to_the_application_and_validate_the_super_button(self):
        """
        DESCRIPTION: Login to the application and validate the super button.
        EXPECTED: Super button should not be displayed.
        """
        pass
