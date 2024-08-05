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
class Test_C44870378_Verify_that_functionality_and_display_of_Help_button_navigation_to_help_page_and_backward_is_as_per_expected(Common):
    """
    TR_ID: C44870378
    NAME: Verify that functionality and display of Help button, navigation to help page and backward is as per expected
    DESCRIPTION: This TC is to verify the functionality of 'Help' when navigated from  quick links under 'Help & Information' from the footer menu.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_verify_the_functionality_help_navigation_to_help_page_and_backward_is_as_per_expected(self):
        """
        DESCRIPTION: Verify the functionality 'Help', navigation to help page and backward is as per expected.
        EXPECTED: User is able to navigate to 'Help' and back to previous page.
        """
        pass
