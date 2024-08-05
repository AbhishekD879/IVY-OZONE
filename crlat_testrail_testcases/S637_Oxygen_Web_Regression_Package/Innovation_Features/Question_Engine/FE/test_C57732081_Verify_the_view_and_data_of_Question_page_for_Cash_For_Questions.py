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
class Test_C57732081_Verify_the_view_and_data_of_Question_page_for_Cash_For_Questions(Common):
    """
    TR_ID: C57732081
    NAME: Verify the view and data of Question page for Cash For Questions
    DESCRIPTION: This test case verifies the view and data of Question page for Cash For Questions.
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
        EXPECTED: 1. The User is redirected to the Question page of Cash For Questions.
        EXPECTED: 2. The Question page is displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d7271e2cba5d54eb5bf0dbf.
        EXPECTED: 3. No Splash page should appear.
        EXPECTED: 4. No Event details (team names, t-shirts, TV-channel, etc.) should appear.
        """
        pass

    def test_003_makes_changes_in_each_field_in_the_cms_and_save_themreload_the_fe(self):
        """
        DESCRIPTION: Makes changes in each field in the CMS and save them.
        DESCRIPTION: Reload the FE.
        EXPECTED: The changes are reflected on the FE.
        """
        pass
