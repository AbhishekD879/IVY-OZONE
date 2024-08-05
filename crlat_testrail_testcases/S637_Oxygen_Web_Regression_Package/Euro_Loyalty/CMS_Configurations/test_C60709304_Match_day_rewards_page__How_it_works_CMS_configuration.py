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
class Test_C60709304_Match_day_rewards_page__How_it_works_CMS_configuration(Common):
    """
    TR_ID: C60709304
    NAME: Match day rewards page - How it works CMS configuration
    DESCRIPTION: This test case is to config how it works text and buttons in CMS
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  configuration for  Euro Loyalty Page should done
    """
    keep_browser_open = True

    def test_001_launch_oxygen_cms_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen CMS application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_click_on_special_pages___match_day_rewards_page_from_left_pane(self):
        """
        DESCRIPTION: Click on special pages - Match day rewards page from left pane
        EXPECTED: Match day rewards page should open with below section
        EXPECTED: > Active - check box
        EXPECTED: > Start date and End date
        EXPECTED: > Table creation
        EXPECTED: > Badge configuration
        EXPECTED: > Messaging
        EXPECTED: > How it works
        EXPECTED: > Terms and conditions
        EXPECTED: > Full terms and conditions URL
        """
        pass

    def test_003_click_on_how_it_works_page(self):
        """
        DESCRIPTION: Click on How it works page
        EXPECTED: How it works page should open with editable rich text box
        """
        pass

    def test_004_enter_text_in_required_format_and_save_changes(self):
        """
        DESCRIPTION: Enter text in required format and save changes
        EXPECTED: Details should be saved successfully
        """
        pass

    def test_005_perform_edit_or_delete_operation_each_section_and_verify(self):
        """
        DESCRIPTION: Perform edit or delete operation each section and verify
        EXPECTED: Details should update accordingly
        """
        pass
