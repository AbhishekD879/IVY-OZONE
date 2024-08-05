import re
import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.p1
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870380_Verify_that_functionality_and_display_of_Contact_Us_button_navigation_to_Contact_Us_page_and_backward_is_as_per_expected(Common):
    """
    TR_ID: C44870380
    NAME: Verify that functionality and display of Contact Us button, navigation to Contact Us page and backward is as per expected
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is opened.
        """
        self.site.wait_content_state('HomePage')

    def test_002_verify_that_functionality_and_display_of_contact_us_button_in_footer_navigation_to_contact_us_page_and_backward_is_as_per_expected(
            self):
        """
        DESCRIPTION: Verify that functionality and display of Contact Us button in Footer, navigation to Contact Us page and backward is as per expected
        EXPECTED: User is able navigate to and from Contact Us page.
        """
        contact_us = self.site.footer.footer_section_top.items_as_ordered_dict.get(vec.BMA.CONTACT_US)
        self.assertTrue(contact_us.is_displayed(), msg=f'"{vec.BMA.CONTACT_US}" is not displayed')
        contact_us.scroll_to_we()
        self.device.driver.implicitly_wait(5)
        contact_us.click()
        wait_for_result(lambda: self.site.direct_chat.topics, timeout=20)
        actual_url = self.device.get_current_url()
        expected_url = re.sub(r"beta2|beta3", "beta", ("https://" + tests.HOSTNAME + "/en/mobileportal/contact"))
        expected_url_beta2 = re.sub(r"beta2|beta3", "beta2", ("https://" + tests.HOSTNAME + "/en/mobileportal/contact"))
        expected_url_beta3 = re.sub(r"beta2|beta3", "beta3", ("https://" + tests.HOSTNAME + "/en/mobileportal/contact"))
        if 'beta2' in tests.HOSTNAME:
            self.assertIn(actual_url, [expected_url, expected_url_beta2],
                          msg=f'Actual url: "{actual_url}" is not same as Expected url: "{[expected_url, expected_url_beta2]}"')
        elif 'beta3' in tests.HOSTNAME:
            self.assertIn(actual_url, [expected_url, expected_url_beta3],
                          msg=f'Actual url: "{actual_url}" is not same as Expected url: "{[expected_url, expected_url_beta3]}"')
        else:
            self.assertEqual(actual_url, expected_url,
                             msg=f'Actual url: "{actual_url}" is not same as Expected url: "{expected_url}"')
        self.device.go_back()
        self.site.wait_content_state(state_name="homepage")
