import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul
from crlat_cms_client.utils.exceptions import CMSException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.homepage
@pytest.mark.banners
@pytest.mark.aem_banners
@pytest.mark.adhoc_suite
@pytest.mark.adhoc06thFeb24
@pytest.mark.promotions_banners_offers
@vtest
# https://jira.corp.entaingroup.com/browse/OZONE-13374
# There is an issue observed on the Coral desktop website where the AEM banner on the home page lacks an active class attribute even when it is active.
# Due to which this test case will fail on Coral desktop.
class Test_C66035620_Verify_scroll_functionality_for_Banners_of_Home_page(Common):
    """
    TR_ID: C66035620
    NAME: Verify scroll functionality for Banners of Home page
    DESCRIPTION: Verify scroll functionality for Banners of Home page
    PRECONDITIONS: 1. Application is launched.
    PRECONDITIONS: 2. Banners are available.
    PRECONDITIONS: 3. Banner carousel time should be configured in Oxygen CMS >System Config > Structure
    """
    keep_browser_open = True

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Application is loaded.
        """
        system_configuration = self.cms_config.get_system_configuration_structure()
        dynamic_banner_details = system_configuration.get('DynamicBanners')
        if not dynamic_banner_details['enabled'] and tests.settings.cms_env == 'prod0':
            raise CMSException('DynamicBanners is not enabled in CMS')
        else:
            self.cms_config.update_system_configuration_structure(config_item='DynamicBanners',
                                                                  field_name='enabled',
                                                                  field_value=True)

        banner_details = system_configuration.get('Banners')
        self.__class__.banner_transition_delay = banner_details.get('transitionDelay')
        if banner_details.get('transitionDelay') == '':
            if tests.settings.cms_env == 'prod0':
                raise CMSException('Banners transitionDelay is not configured in CMS')
            else:
                self.__class__.banner_transition_delay = self.cms_config.update_system_configuration_structure(config_item='Banners',
                                                                  field_name='transitionDelay',
                                                                  field_value='5000').get('structure').get('Banners').get('transitionDelay')

        self.site.wait_content_state('HomePage')
        result = self.site.contents.aem_banner_section.wait_for_banners()
        self.assertTrue(result, msg='AEM Banners are not displayed')

    def test_002_scroll_through_the_banners_on_home_page(self):
        """
        DESCRIPTION: Scroll through the Banners on Home page.
        EXPECTED: User is able to scroll right &amp; left and view all the available banners
        """
        if self.device_type == 'desktop':
            self.site.contents.aem_banner_section.mouse_over()
            self.assertTrue(self.site.contents.aem_banner_section.has_arrow_next, msg='No > arrow found')
            self.site.contents.aem_banner_section.arrow_next.click()
            self.assertTrue(self.site.contents.aem_banner_section.has_arrow_previous, msg='No < arrow found')

            self.site.contents.aem_banner_section.mouse_over()
            self.site.contents.aem_banner_section.arrow_next.click()
            current_active_banner_name = self.site.contents.aem_banner_section.active_banner_name

            self.site.contents.aem_banner_section.arrow_next.click()
            after_clicking_arrow_next_active_banner_name = self.site.contents.aem_banner_section.active_banner_name
        else:
            current_active_banner_name = self.site.contents.aem_banner_section.active_banner_name

            all_non_active_slide_buttons = list(self.site.contents.aem_banner_section.non_active_slide_buttons.items())
            all_non_active_slide_buttons[len(all_non_active_slide_buttons) - 1][1].click()

            after_clicking_arrow_next_active_banner_name = self.site.contents.aem_banner_section.active_banner_name

        self.assertNotEqual(current_active_banner_name, after_clicking_arrow_next_active_banner_name,
                            msg=f'current active banner name: "{current_active_banner_name}" '
                                f'and after clicking arrow next active banner name: '
                                f'"{after_clicking_arrow_next_active_banner_name}" both are not expected to be same')

    def test_003_click_on_any_of_the_banner(self):
        """
        DESCRIPTION: Click on any of the Banner
        EXPECTED: User is redirected to the configured URL.
        """
        url_before_click = self.device.get_current_url()
        self.site.contents.aem_banner_section.active_banner.mouse_over()
        self.site.contents.aem_banner_section.active_banner.click()
        self.__class__.number_of_open_tabs = self.device.get_number_of_tabs()
        if self.number_of_open_tabs > 1:
            self.device.switch_to_new_tab()
            url_after_click = self.device.get_current_url()
            self.device.close_current_tab()
            self.device.switch_to_new_tab()
        else:
            self.site.wait_content_state_changed()
            url_after_click = self.device.get_current_url()

        self.assertNotEqual(url_before_click, url_after_click,
                            msg=f'URL "{url_before_click}" before click is same as URL "{url_after_click}" after click')


    def test_004_navigate_back_to_home_page_from_any_of_the_slp(self):
        """
        DESCRIPTION: Navigate back to home page from any of the SLP
        EXPECTED: Home page is loaded
        """
        if not self.number_of_open_tabs > 1:
            self.device.go_back()
        self.site.wait_content_state('HomePage')

    def test_005_scroll_through_the_banners_on_home_page(self):
        """
        DESCRIPTION: Scroll through the Banners on Home page.
        EXPECTED: User is able to scroll right &amp; left and view all the available banners.
        """
        if self.device_type == 'desktop':
            self.site.contents.aem_banner_section.mouse_over()
            self.assertTrue(self.site.contents.aem_banner_section.has_arrow_next, msg='No > arrow found')
            self.site.contents.aem_banner_section.arrow_next.click()
            self.assertTrue(self.site.contents.aem_banner_section.has_arrow_previous, msg='No < arrow found')

            self.site.contents.aem_banner_section.mouse_over()
            self.site.contents.aem_banner_section.arrow_next.click()
            current_active_banner_name = self.site.contents.aem_banner_section.active_banner_name

            self.site.contents.aem_banner_section.arrow_next.click()
            after_clicking_arrow_next_active_banner_name = self.site.contents.aem_banner_section.active_banner_name
        else:
            current_active_banner_name = self.site.contents.aem_banner_section.active_banner_name

            all_non_active_slide_buttons = list(self.site.contents.aem_banner_section.non_active_slide_buttons.items())
            all_non_active_slide_buttons[len(all_non_active_slide_buttons) - 1][1].click()

            after_clicking_arrow_next_active_banner_name = self.site.contents.aem_banner_section.active_banner_name

        self.assertNotEqual(current_active_banner_name, after_clicking_arrow_next_active_banner_name,
                            msg=f'current active banner name: {current_active_banner_name}'
                                f'and after clicking arrow next active banner name:'
                                f'{after_clicking_arrow_next_active_banner_name} both are not expected to be same')

    def test_006_based_on_the_default_time_set_in_cms_scroll_should_move(self):
        """
        DESCRIPTION: Based on the default time set in cms, scroll should move.
        EXPECTED: Scroll should be able to move based on the time limit set on cms.
        """
        current_active_banner_name = self.site.contents.aem_banner_section.active_banner_name
        wait_for_haul((int(self.banner_transition_delay) / 1000) + 3)  # converting received CMS time to seconds and waiting that long
        after_banner_transition_delay_active_banner_name = self.site.contents.aem_banner_section.active_banner_name

        self.assertNotEqual(current_active_banner_name, after_banner_transition_delay_active_banner_name,
                            msg=f'current active banner name: {current_active_banner_name}'
                                f'and after clicking arrow next active banner name:'
                                f'{after_banner_transition_delay_active_banner_name} both are not expected to be same')
