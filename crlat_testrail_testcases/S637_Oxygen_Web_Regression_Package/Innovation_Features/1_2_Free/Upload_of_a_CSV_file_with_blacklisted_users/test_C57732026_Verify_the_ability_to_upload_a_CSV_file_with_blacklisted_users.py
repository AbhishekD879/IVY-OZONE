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
class Test_C57732026_Verify_the_ability_to_upload_a_CSV_file_with_blacklisted_users(Common):
    """
    TR_ID: C57732026
    NAME: Verify the ability to upload a CSV file with blacklisted users
    DESCRIPTION: This test case verifies the ability to upload a CSV file with black listed users.
    PRECONDITIONS: 1. The CSV file with blacklisted users is present on your computer.
    PRECONDITIONS: 2. Open the Oxygen CMS.
    PRECONDITIONS: 3. Navigate to the '1-2-Free' module.
    PRECONDITIONS: 4. Select the 'Qualification Rule' subsection.
    PRECONDITIONS: 5. Navigate to the 'Upload Blacklisted Users [CSV]' row.
    """
    keep_browser_open = True

    def test_001_click_on_the_upload_file_button(self):
        """
        DESCRIPTION: Click on the 'Upload File' button.
        EXPECTED: The Pop-up with is opened.
        """
        pass

    def test_002_select_a_csv_file_from_your_computer(self):
        """
        DESCRIPTION: Select a CSV file from your computer.
        EXPECTED: The 'Open' button is activated.
        """
        pass

    def test_003_click_on_the_open_button(self):
        """
        DESCRIPTION: Click on the 'Open' button.
        EXPECTED: The Pop-up with is closed.
        EXPECTED: The name of the CSV file is displayed in the 'Upload Blacklisted Users [CSV]' row.
        """
        pass

    def test_004_click_on_the_save_changes_button(self):
        """
        DESCRIPTION: Click on the 'Save Changes' button.
        EXPECTED: The 'Saving of: Qualification Rule' pop-up with is opened.
        """
        pass

    def test_005_click_on_the_yes_button(self):
        """
        DESCRIPTION: Click on the 'Yes' button.
        EXPECTED: The 'Your changes have been saved' message is displayed.
        """
        pass
