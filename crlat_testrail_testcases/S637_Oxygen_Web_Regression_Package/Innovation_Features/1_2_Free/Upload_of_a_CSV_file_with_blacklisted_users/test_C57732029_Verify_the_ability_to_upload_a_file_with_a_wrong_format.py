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
class Test_C57732029_Verify_the_ability_to_upload_a_file_with_a_wrong_format(Common):
    """
    TR_ID: C57732029
    NAME: Verify the ability to upload a file with a wrong format
    DESCRIPTION: This test case verifies the ability to upload a file with a wrong format.
    PRECONDITIONS: 1. The file with wrong format (any format, except a CSV) is present on your computer.
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

    def test_002_select_a_file_with_wrong_format_from_your_computer(self):
        """
        DESCRIPTION: Select a file with wrong format from your computer.
        EXPECTED: The 'Error. Unsupported file type.' pop-up is occurred.
        """
        pass

    def test_003_click_on_the_ok_button(self):
        """
        DESCRIPTION: Click on the 'OK' button.
        EXPECTED: The 'Error. Unsupported file type.' pop-up is closed.
        EXPECTED: The 'Upload Blacklisted Users [CSV]' row is empty.
        """
        pass
