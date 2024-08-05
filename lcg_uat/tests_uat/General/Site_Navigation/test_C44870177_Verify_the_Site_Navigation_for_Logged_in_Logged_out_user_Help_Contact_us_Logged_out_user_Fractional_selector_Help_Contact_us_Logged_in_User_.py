import voltron.environments.constants as vec
import pytest
import tests
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared.components.base import ComponentBase


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870177_Verify_the_Site_Navigation_for_Logged_in_Logged_out_user_Help_Contact_us_Logged_out_user_Fractional_selector_Help_Contact_us_Logged_in_User_(Common, ComponentBase):
    """
    TR_ID: C44870177
    NAME: "Verify the Site Navigation for Logged in/Logged out user -Help/Contact us (Logged out user) -Fractional selector/Help/Contact us ( Logged in User) "
    DESCRIPTION: "Verify the Site Navigation for Logged in/Logged out user
    DESCRIPTION: -Help/Contact us (Logged out user)
    DESCRIPTION: -Fractional selector/Help/Contact us ( Logged in User)
    """
    keep_browser_open = True

    def verify_help_contact_page(self):
        wait_for_result(lambda: self.site.direct_chat.topics, timeout=20)
        actual_url = self.device.get_current_url()
        expected_url = "https://" + tests.HOSTNAME + "/en/mobileportal/contact"
        self.assertEqual(actual_url, expected_url,
                         msg=f'Actual url: "{actual_url}" is not same as'
                             f'Expected url: "{expected_url}"')
        if self.device_type == 'mobile':
            self.site.direct_chat.close_button.click()
        else:
            self.device.go_back()

    def select_odd_format_and_check_price_button_accordingly(self, decimal=False):
        self.navigate_to_page('settings')
        if decimal:
            format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
            self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        else:
            format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
            self.assertTrue(format_changed, msg='Odds format is not changed to fractional')
        self.site.back_button.click()
        self.site.wait_content_state_changed(timeout=10)
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state('Football')
        outputprices = self.get_output_prices_values(section_name='MATCHES')
        for price in outputprices.values():
            self._logger.info(f'Current price is: "{price}"')
            if decimal:
                self.assertRegexpMatches(price, self.decimal_pattern,
                                         msg=f'Price/Odds value "{price}" '
                                             f'not match decimal pattern: "{self.decimal_pattern}"')
            else:
                self.assertRegexpMatches(price, self.fractional_pattern,
                                         msg=f'Price/Odds value "{price}" '
                                             f'not match fractional pattern: "{self.fractional_pattern}"')

    def test_001_load_app_and_click_on_contact_us_from_bottom_menu_for_logged_out_user_on_mobile(self):
        """
        DESCRIPTION: Load app and click on 'Contact US' from bottom menu for Logged out user on mobile
        EXPECTED: User should navigate to https://beta-sports.coral.co.uk/en/mobileportal/contact
        EXPECTED: User should be able to close this overlay window by tapping on 'X' (Applicable to Mobile only)
        """
        self.site.wait_content_state('Homepage')
        contact_us = self.site.footer.footer_section_top.items_as_ordered_dict.get(vec.BMA.CONTACT_US)
        self.assertTrue(contact_us.is_displayed(), msg=f'"{vec.BMA.CONTACT_US}" is not displayed')
        contact_us.click()
        self.verify_help_contact_page()

    def test_002_click_on_contact_us_from_the_footer_menu_for_logged_out_user_on_desktop__tablet(self):
        """
        DESCRIPTION: click on 'Contact US' from the Footer menu for Logged out user on Desktop & Tablet
        EXPECTED: User should navigate to https://beta-sports.coral.co.uk/en/mobileportal/contact
        EXPECTED: No 'X' button available on Desktop and Tablet
        """
        # this step is covered in step-1

    def test_003_click_on_help__contact_from_right_menu_for_logged_in_user_on_mobile(self):
        """
        DESCRIPTION: Click on 'Help & Contact' from Right menu for Logged in user on mobile
        EXPECTED: User should navigate to https://beta-sports.coral.co.uk/en/mobileportal/contact
        EXPECTED: User should be able to close this overlay window by tapping on 'X'
        """
        self.site.wait_content_state('Homepage', timeout=5)
        self.site.login(timeout_wait_for_dialog=10)
        self.site.wait_content_state('Homepage')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right Menu')
        self.site.right_menu.click_item('Help & Contact')
        self.verify_help_contact_page()
        if self.device_type == 'mobile':
            self.site.right_menu.close_icon.click()
        self.site.wait_content_state_changed(timeout=5)

    def test_004_click_on_help__contact_from_right_menu_for_logged_in_user_on_desktop__tablet(self):
        """
        DESCRIPTION: Click on 'Help & Contact' from Right menu for Logged in user on Desktop & Tablet
        EXPECTED: User should navigate to https://beta-sports.coral.co.uk/en/mobileportal/contact
        EXPECTED: No 'X' button available on Desktop and Tablet
        """
        # this is covered in step-3

    def test_005_click_on_the_avatar__settings__betting_settings(self):
        """
        DESCRIPTION: Click on the Avatar > Settings > Betting Settings
        EXPECTED: User should see the contents of settings. User should be able set odds to Fractional / Decimal
        """
        self.select_odd_format_and_check_price_button_accordingly()

    def test_006_verify_odds_on_the_site_after_setting_the_fractional_selector__decimal_selector_respectively(self):
        """
        DESCRIPTION: Verify Odds on the site after setting the fractional selector & decimal selector respectively
        EXPECTED: User should see all the odds in Fractional if odds are set to Fractional in Settings.
        EXPECTED: User should see all the odds in Decimal if odds are set to Decimal in Settings.
        """
        self.select_odd_format_and_check_price_button_accordingly(decimal=True)
