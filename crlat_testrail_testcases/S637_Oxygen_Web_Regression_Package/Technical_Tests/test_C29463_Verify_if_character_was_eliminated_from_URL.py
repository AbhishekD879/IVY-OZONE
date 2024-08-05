import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29463_Verify_if_character_was_eliminated_from_URL(Common):
    """
    TR_ID: C29463
    NAME: Verify if '#' character was eliminated from URL
    DESCRIPTION: This test case verifies if '#' character was eliminated from URL.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_verify_url_for_homepage(self):
        """
        DESCRIPTION: Verify URL for Homepage
        EXPECTED: * '#' character is NOT displayed anymore in URL row
        EXPECTED: * App link is displayed, for example, in the following format: https://invictus.coral.co.uk
        """
        pass

    def test_003_verify_url_for_other_pages_in_the_application(self):
        """
        DESCRIPTION: Verify URL for other pages in the application
        EXPECTED: * '#' character is NOT displayed anymore in URL row
        EXPECTED: * User is successfully redirected to the particular page
        """
        pass

    def test_004_add__manually_when_the_user_is_locating_on_some_of_the_app_pages_except_homepage(self):
        """
        DESCRIPTION: Add '#' manually when the user is locating on some of the app pages (except Homepage)
        EXPECTED: * '#' character is removed automatically from URL row
        EXPECTED: * Particular page is loaded successfully
        """
        pass
