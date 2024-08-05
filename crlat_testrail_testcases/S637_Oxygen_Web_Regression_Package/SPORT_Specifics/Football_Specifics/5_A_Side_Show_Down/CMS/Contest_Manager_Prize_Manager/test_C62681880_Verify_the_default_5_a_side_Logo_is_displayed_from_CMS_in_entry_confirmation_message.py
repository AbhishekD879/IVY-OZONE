import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C62681880_Verify_the_default_5_a_side_Logo_is_displayed_from_CMS_in_entry_confirmation_message(Common):
    """
    TR_ID: C62681880
    NAME: Verify the default 5-a-side Logo is displayed from CMS in entry confirmation message
    DESCRIPTION: This test case Verifies default 5-a-side Logo is displayed from CMS in entry confirmation message
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Image manager
    PRECONDITIONS: 1. 5-a-side logo is pulled from Image manager
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached"
    """
    keep_browser_open = True

    def test_001_login_to_cms_ladbrokes_application_with_admin_access(self):
        """
        DESCRIPTION: Login to CMS Ladbrokes application with admin access
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_image_manager_and_add_5_a_side_logo_image(self):
        """
        DESCRIPTION: Navigate to Image manager and add 5-a-side logo image
        EXPECTED: user should able to navigate to image manager and able to upload 5-a-side logo
        EXPECTED: ![](index.php?/attachments/get/171309008)
        """
        pass

    def test_003_validate_5_a_side_logo_for_the_active_contest_in_fe_after_placing_a_bet(self):
        """
        DESCRIPTION: Validate 5-a-side logo for the active contest in FE after placing a bet
        EXPECTED: Uploaded 5-a-side image should display in entry confirmation message for valid bet receipt
        EXPECTED: ![](index.php?/attachments/get/171309009)
        """
        pass
