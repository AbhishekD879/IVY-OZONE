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
class Test_C44870350_Verify_the_functionality_for_marketing_contact_preferences(Common):
    """
    TR_ID: C44870350
    NAME: Verify the functionality for marketing/contact preferences.
    DESCRIPTION: 
    PRECONDITIONS: Load the application/site and the
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_click_on_the_avatar__settings__marketing_preferences(self):
        """
        DESCRIPTION: Click on the Avatar > Settings > Marketing Preferences.
        EXPECTED: Communication preferences are displayed.
        """
        pass

    def test_002_select_all_and_verify(self):
        """
        DESCRIPTION: Select 'All' and verify.
        EXPECTED: 1. The message indicating that the preferences have been updated is displayed.
        EXPECTED: 2. All the contact options/boxes are checked.
        """
        pass

    def test_003_de_select_all_and_select_email_verify(self):
        """
        DESCRIPTION: De-select 'All' and select 'Email'. Verify.
        EXPECTED: 1. The message indicating that the preferences have been updated is displayed.
        EXPECTED: 2. The box/option for 'Email' is checked, remaining boxes/options are not selected/checked.
        """
        pass

    def test_004_click_on_save_button_and_navigate_to_marketing_preferences_again_verify(self):
        """
        DESCRIPTION: Click on Save button and navigate to Marketing preferences again. Verify.
        EXPECTED: The box/option for 'Email' is checked, remaining boxes/options are not selected/checked.
        """
        pass
