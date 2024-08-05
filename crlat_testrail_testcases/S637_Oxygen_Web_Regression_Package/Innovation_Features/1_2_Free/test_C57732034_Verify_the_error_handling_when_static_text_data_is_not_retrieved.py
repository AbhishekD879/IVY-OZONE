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
class Test_C57732034_Verify_the_error_handling_when_static_text_data_is_not_retrieved(Common):
    """
    TR_ID: C57732034
    NAME: Verify the error handling when static text data is not retrieved
    DESCRIPTION: This test case verifies the error handling when static text data is not retrieved.
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. The Quick link 'Play 1-2-FREE predictor and win £150' is available on the Home page / Football page.
    PRECONDITIONS: 3. Open the Oxygen CMS.
    PRECONDITIONS: 4. Navigate to the 1-2-Free section.
    PRECONDITIONS: 5. Select the 'Static Text' subsection.
    PRECONDITIONS: 6. Select 'Current week' tab.
    PRECONDITIONS: 7. Uncheck the 'Active' checkbox.
    PRECONDITIONS: 8. Click on the 'Save Changes' button.
    PRECONDITIONS: 9. Click on the 'Yes' button in the 'Saving of: Current week tab' pop-up.
    PRECONDITIONS: 10. Click on the 'Yes' button in the 'Upload Completed' pop-up.
    """
    keep_browser_open = True

    def test_001_open_the_website__app(self):
        """
        DESCRIPTION: Open the website / app.
        EXPECTED: The website / app is opened.
        """
        pass

    def test_002_tap_on_the_1_2_free_link(self):
        """
        DESCRIPTION: Tap on the '1-2-Free' link.
        EXPECTED: The Error message with 'Go back' button is displayed.
        """
        pass

    def test_003_tap_on_the_go_back_button(self):
        """
        DESCRIPTION: Tap on the 'Go back' button.
        EXPECTED: The User is redirected to the Home page / Football page.
        """
        pass
