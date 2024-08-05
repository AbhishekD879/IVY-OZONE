import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65934236_Verify_updated_details_of_super_button_is_displaying_in_FE(Common):
    """
    TR_ID: C65934236
    NAME: Verify updated details of super button is displaying in FE.
    DESCRIPTION: This test case is to validate the edit functionality of description of existing super button.
    PRECONDITIONS: Active Super button should be configured in CMS
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

    def test_003_now_go_to_cmsgthome_page_modulegtsuper_button_screen_and_click_on_configured_super_button_name(self):
        """
        DESCRIPTION: Now go to CMS&gt;Home page module&gt;Super button screen and click on configured super button name.
        EXPECTED: Super button details should be displayed.
        """
        pass

    def test_004_now_edit_the_data_in_description_and_theme_fields_and_save_it(self):
        """
        DESCRIPTION: Now edit the data in description and Theme fields and save it.
        EXPECTED: Details should be saved successfully.
        """
        pass

    def test_005_go_to_fe_and_validate_the_description_and_theme_of_the_super_button(self):
        """
        DESCRIPTION: Go to FE and validate the description and theme of the super button.
        EXPECTED: Updated description details and Theme should be reflected in FE.
        """
        pass

    def test_006_login_to_the_application_and_validate_the_super_button(self):
        """
        DESCRIPTION: Login to the application and validate the super button.
        EXPECTED: Updated description details and Theme should be reflected in FE.
        """
        pass
