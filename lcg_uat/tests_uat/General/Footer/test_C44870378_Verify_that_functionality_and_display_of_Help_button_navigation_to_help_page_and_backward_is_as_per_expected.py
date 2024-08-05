import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


# @pytest.mark.uat
@pytest.mark.desktop
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.p1
@pytest.mark.other
@vtest
class Test_C44870378_Verify_that_functionality_and_display_of_Help_button_navigation_to_help_page_and_backward_is_as_per_expected(Common):
    """
    TR_ID: C44870378
    NAME: Verify that functionality and display of Help button, navigation to help page and backward is as per expected
    DESCRIPTION: This TC is to verify the functionality of 'Visit our Help Centre'.
    """
    keep_browser_open = True

    def test_001_verify_the_functionality_visit_our_help_centre_navigation_to_help_page_and_backward_is_as_per_expected(self):
        """
        DESCRIPTION: Verify the functionality 'Visit Our Help Centre', navigation to help page and backward is as per expected.
        EXPECTED: User is able to navigate to 'Visit Our Help Centre' and back to previous page.
        """
        self.site.wait_content_state("HomePage")
        help_link = self.site.footer.footer_section_top.items_as_ordered_dict.get(vec.BMA.CONTACT_US)
        self.assertTrue(help_link.is_displayed(), msg='"Help button" is not displayed')
        help_link.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/contact'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=20)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg=f'"{vec.BMA.CONTACT_US}" page is not found')
        self.device.go_back()
        self.site.wait_content_state('Homepage')
