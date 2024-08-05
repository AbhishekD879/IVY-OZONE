import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870380_Verify_that_functionality_and_display_of_Contact_Us_button_navigation_to_Contact_Us_page_and_backward_is_as_per_expected(Common):
    """
    TR_ID: C44870380
    NAME: Verify that functionality and display of Contact Us button, navigation to Contact Us page and backward is as per expected
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is opened.
        """
        pass

    def test_002_verify_that_functionality_and_display_of_contact_us_button_in_footer_navigation_to_contact_us_page_and_backward_is_as_per_expected(self):
        """
        DESCRIPTION: Verify that functionality and display of Contact Us button in Footer, navigation to Contact Us page and backward is as per expected
        EXPECTED: User is able navigate to and from Contact Us page.
        """
        pass
