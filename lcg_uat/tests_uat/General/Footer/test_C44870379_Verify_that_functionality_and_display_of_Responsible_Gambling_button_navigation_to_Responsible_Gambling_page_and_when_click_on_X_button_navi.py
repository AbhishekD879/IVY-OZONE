import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.uat
# @pytest.mark.p1
# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870379_Verify_that_functionality_and_display_of_Responsible_Gambling_button_navigation_to_Responsible_Gambling_page_and_when_click_on_X_button_navigate_back_to_sportsbook_application(Common):
    """
    TR_ID: C44870379
    NAME: Verify that functionality and display of Responsible Gambling button, navigation to Responsible Gambling page and when click on 'X' button navigate back to sportsbook application
    DESCRIPTION: Verify that functionality and display of Responsible Gambling button, navigation to Responsible Gambling page and when click on 'X' button navigate back to sportsbook application
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is loaded.
        """
        self.site.wait_content_state('HomePage')

    def test_002_verify_that_functionality_and_display_of_responsible_gambling_button(self):
        """
        DESCRIPTION: Verify that functionality and display of Responsible Gambling button, navigation to Responsible Gambling page and when click on '<--' button navigate back to sportsbook application
        EXPECTED: User is able to navigate to Responsible Gambling and back to previous page by clicking back arrow. (May be different for different devices)
        """
        responsible_gambling = self.site.footer.footer_section_top.items_as_ordered_dict.get(vec.BMA.MY_ACC_RESPONSIBLEGAMBLING.title())
        self.assertTrue(responsible_gambling.is_displayed(),
                        msg='Responsible gambling is not displayed')
        responsible_gambling.click()
        self.device.driver.implicitly_wait(5)

        if self.brand == 'ladbrokes':
            self.device.switch_to_new_tab()

        if self.device_type == 'mobile':
            actual_title = self.site.responsible_gaming.header_title
            self.assertEqual(actual_title.lower(), vec.BMA.EXPECTED_LINKS_LIST.responsible_gambling.lower(),
                             msg=f'Actual title {actual_title} is not as same as'
                                 f'Expected title {vec.BMA.EXPECTED_LINKS_LIST.responsible_gambling.lower()}')
        else:
            gambling_page = self.site.responsible_gaming
            self.assertTrue(gambling_page, msg='Responsible gambling is not displayed')

        if self.brand == 'bma':
            self.device.go_back()
        else:
            self.device.close_current_tab()
            self.device.open_tab(0)
        self.site.wait_content_state('HomePage')
