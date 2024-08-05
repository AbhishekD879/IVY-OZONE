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
class Test_C57732030_Verify_the_ability_to_change_a_CSV_file_with_blacklisted_users(Common):
    """
    TR_ID: C57732030
    NAME: Verify the ability to change a CSV file with blacklisted users
    DESCRIPTION: This test case verifies the ability to change a CSV file with black listed users.
    PRECONDITIONS: 1. A CSV file with blacklisted users is present on your computer.
    PRECONDITIONS: 2. Open the Oxygen CMS.
    PRECONDITIONS: 3. Navigate to the '1-2-Free' module.
    PRECONDITIONS: 4. Select the 'Qualification Rule' subsection.
    PRECONDITIONS: 5. Navigate to the 'Upload Blacklisted Users [CSV]' row.
    PRECONDITIONS: 6. Click on the 'Upload File' button.
    PRECONDITIONS: 7. Select a CSV file from your computer.
    PRECONDITIONS: 8. Click on the 'Save Changes' button.
    PRECONDITIONS: 9. Click on the 'Yes' button in the 'Saving of: Qualification Rule' pop-up.
    """
    keep_browser_open = True

    def test_001_click_on_the_change_file_button(self):
        """
        DESCRIPTION: Click on the 'Change File' button.
        EXPECTED: The Pop-up with is opened.
        """
        pass

    def test_002_select_a_csv_file_from_your_computer(self):
        """
        DESCRIPTION: Select a CSV file from your computer.
        EXPECTED: The CSV file is successfully selected.
        """
        pass

    def test_003_click_on_the_save_changes_button(self):
        """
        DESCRIPTION: Click on the 'Save Changes' button.
        EXPECTED: The 'Saving of: Qualification Rule' pop-up with is opened.
        """
        pass

    def test_004_click_on_the_yes_button(self):
        """
        DESCRIPTION: Click on the 'Yes' button.
        EXPECTED: The 'Your changes have been saved' message is displayed.
        """
        pass
