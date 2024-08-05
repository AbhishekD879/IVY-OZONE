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
class Test_C57732082_Verify_the_view_and_data_of_End_page_for_Cash_for_Questions(Common):
    """
    TR_ID: C57732082
    NAME: Verify the view and data of End page for Cash for Questions
    DESCRIPTION: This test case verifies the view and data of End page for Cash for Questions.
    PRECONDITIONS: 1. CMS User is logged in.
    PRECONDITIONS: 2. An active Quiz is configured.
    PRECONDITIONS: 3. Navigate to the 'Quiz Configuration tab.
    PRECONDITIONS: 4. Set all toggles off, except the 'Show Progress bar' and 'Use back button to exit and hide X button'.
    PRECONDITIONS: 5. Save the changes.
    PRECONDITIONS: 6. The User is logged in.
    """
    keep_browser_open = True

    def test_001_navigate_to_the_page_which_is_configured_in_the_cms_to_trigger_the_quiz_pop_up_eg_football_page(self):
        """
        DESCRIPTION: Navigate to the page, which is configured in the CMS to trigger the Quiz pop-up (e.g. Football page).
        EXPECTED: The Quiz pop-up is opened.
        """
        pass

    def test_002_tap_the_take_a_quiz_cta_button(self):
        """
        DESCRIPTION: Tap the 'Take a Quiz' CTA button.
        EXPECTED: The User is redirected to the Question page of Cash For Questions.
        """
        pass

    def test_003_select_the_1st_option_to_trigger_the_end_page_1(self):
        """
        DESCRIPTION: Select the 1st Option to trigger the End page #1.
        EXPECTED: The End page page is displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d7271e2ccb615186fb53d47.
        """
        pass

    def test_004_makes_changes_in_each_field_in_the_cms_and_save_themreload_the_fe(self):
        """
        DESCRIPTION: Makes changes in each field in the CMS and save them.
        DESCRIPTION: Reload the FE.
        EXPECTED: The changes are reflected on the FE.
        """
        pass

    def test_005_logout_and_login_with_the_credentials_of_the_user_2(self):
        """
        DESCRIPTION: Logout and login with the credentials of the User #2.
        EXPECTED: The User is successfully logged in.
        """
        pass

    def test_006_navigate_to_the_page_which_is_configured_in_the_cms_to_trigger_the_quiz_pop_up_eg_football_page(self):
        """
        DESCRIPTION: Navigate to the page, which is configured in the CMS to trigger the Quiz pop-up (e.g. Football page).
        EXPECTED: The Quiz pop-up is opened.
        """
        pass

    def test_007_tap_the_take_a_quiz_cta_button(self):
        """
        DESCRIPTION: Tap the 'Take a Quiz' CTA button.
        EXPECTED: The User is redirected to the Question page of Cash For Questions.
        """
        pass

    def test_008_select_the_1st_option_to_trigger_the_end_page_2(self):
        """
        DESCRIPTION: Select the 1st Option to trigger the End page #2.
        EXPECTED: The End page page is displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d7271e2039b774ecd527748.
        """
        pass

    def test_009_makes_changes_in_each_field_in_the_cms_and_save_themreload_the_fe(self):
        """
        DESCRIPTION: Makes changes in each field in the CMS and save them.
        DESCRIPTION: Reload the FE.
        EXPECTED: The changes are reflected on the FE.
        """
        pass
