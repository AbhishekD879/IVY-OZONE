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
class Test_C57732100_Verify_the_Quiz_Popup_is_not_displayed_when_the_Quiz_Popup_is_active(Common):
    """
    TR_ID: C57732100
    NAME: Verify the Quiz Popup is not displayed when the Quiz Popup is active
    DESCRIPTION: This test case verifies that the Quiz Popup is nod displayed after proceeding to the Sport page when:
    DESCRIPTION: - the Quiz Popup is active,
    DESCRIPTION: - the User is logged in,
    DESCRIPTION: - the User proceeds to the Sport page which was not configured in the Quiz Popup.
    PRECONDITIONS: 1. The CMS User has configured the Quiz Popup for a Tennis page.
    PRECONDITIONS: 2. The Quiz Popup is active.
    PRECONDITIONS: 3. The User is logged in.
    """
    keep_browser_open = True

    def test_001_open_a_sport_page_which_was_not_configured_in_the_quiz_popup(self):
        """
        DESCRIPTION: Open a Sport page, which was not configured in the Quiz Popup.
        EXPECTED: The Quiz Popup is not displayed.
        """
        pass
