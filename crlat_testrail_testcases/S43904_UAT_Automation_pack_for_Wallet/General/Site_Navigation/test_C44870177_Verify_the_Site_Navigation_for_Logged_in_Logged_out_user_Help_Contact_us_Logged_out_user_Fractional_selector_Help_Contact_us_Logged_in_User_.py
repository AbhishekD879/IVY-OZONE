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
class Test_C44870177_Verify_the_Site_Navigation_for_Logged_in_Logged_out_user_Help_Contact_us_Logged_out_user_Fractional_selector_Help_Contact_us_Logged_in_User_(Common):
    """
    TR_ID: C44870177
    NAME: "Verify the Site Navigation for Logged in/Logged out user -Help/Contact us (Logged out user) -Fractional selector/Help/Contact us ( Logged in User) "
    DESCRIPTION: "Verify the Site Navigation for Logged in/Logged out user
    DESCRIPTION: -Help/Contact us (Logged out user)
    DESCRIPTION: -Fractional selector/Help/Contact us ( Logged in User)
    DESCRIPTION: "
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_app_and_click_on_contact_us_from_bottom_menu_for_logged_out_user_on_mobile(self):
        """
        DESCRIPTION: Load app and click on 'Contact US' from bottom menu for Logged out user on mobile
        EXPECTED: User should navigate to https://beta-sports.coral.co.uk/en/mobileportal/contact
        EXPECTED: User should be able to close this overlay window by tapping on 'X' (Applicable to Mobile only)
        """
        pass

    def test_002_click_on_contact_us_from_the_footer_menu_for_logged_out_user_on_desktop__tablet(self):
        """
        DESCRIPTION: click on 'Contact US' from the Footer menu for Logged out user on Desktop & Tablet
        EXPECTED: User should navigate to https://beta-sports.coral.co.uk/en/mobileportal/contact
        EXPECTED: No 'X' button available on Desktop and Tablet
        """
        pass

    def test_003_click_on_help__contact_from_right_menu_for_logged_in_user_on_mobile(self):
        """
        DESCRIPTION: Click on 'Help & Contact' from Right menu for Logged in user on mobile
        EXPECTED: User should navigate to https://beta-sports.coral.co.uk/en/mobileportal/contact
        EXPECTED: User should be able to close this overlay window by tapping on 'X'
        """
        pass

    def test_004_click_on_help__contact_from_right_menu_for_logged_in_user_on_desktop__tablet(self):
        """
        DESCRIPTION: Click on 'Help & Contact' from Right menu for Logged in user on Desktop & Tablet
        EXPECTED: User should navigate to https://beta-sports.coral.co.uk/en/mobileportal/contact
        EXPECTED: No 'X' button available on Desktop and Tablet
        """
        pass

    def test_005_click_on_the_avatar__settings__betting_settings(self):
        """
        DESCRIPTION: Click on the Avatar > Settings > Betting Settings
        EXPECTED: User should see the contents of settings. User should be able set odds to Fractional / Decimal
        """
        pass

    def test_006_verify_odds_on_the_site_after_setting_the_fractional_selector__decimal_selector_respectively(self):
        """
        DESCRIPTION: Verify Odds on the site after setting the fractional selector & decimal selector respectively
        EXPECTED: User should see all the odds in Fractional if odds are set to Fractional in Settings.
        EXPECTED: User should see all the odds in Decimal if odds are set to Decimal in Settings.
        """
        pass
