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
class Test_C1501092_Tracking_of_Cookies_Policies_Banner_actions(Common):
    """
    TR_ID: C1501092
    NAME: Tracking of 'Cookies' Policies Banner actions
    DESCRIPTION: This test case verifies GA tracking of 'Cookies' Policies Banner actions:
    DESCRIPTION: - when user is logged - out
    DESCRIPTION: - when user logs in: the updated policy banner is showing together with cookie policy banner for active opt-in user
    DESCRIPTION: - when user logs in: the updated policy banner is showing together with cookie policy banner for inactive opt-in user
    DESCRIPTION: - when user logs in: the updated policy banner is showing together with cookie policy banner for opt-out user
    PRECONDITIONS: 1.	Test Case should be executed on  mobile, tablet & desktop platforms
    PRECONDITIONS: 2.	Dev Tools -> Console should be opened
    PRECONDITIONS: 3.	Instruction for real mobile devices/ wrappers debugging: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: Clear browsing data (For each test run and user type).
    PRECONDITIONS: Instructions on how to trigger active opt-in updated policy banner are detailed in TC [C1474024]
    PRECONDITIONS: Instructions on how to trigger inactive opt-in updated policy banner are detailed in TC [C1474025]
    PRECONDITIONS: Instructions on how to trigger opt-out updated policy banner are detailed inTC [C1474610]
    PRECONDITIONS: **NOTE-Important**: For the URL links clicks (privacy and cookie policies links), the tracked **eventlabel value** in dataLayer will be based on the title attribute text in the respective banner’s CMS static block. Thus the eventLabel may change from the one recorded in current test case, in case the TitleID will be changed in the future in CMS. Always check this title in CMs before running the test case.
    """
    keep_browser_open = True

    def test_001_load_the_app_and_make_sure_cookie_banner_is_shown_for_guest_user(self):
        """
        DESCRIPTION: Load the app and make sure cookie banner is shown for guest user
        EXPECTED: Cookie policy banner is displayed
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'cookie',
        EXPECTED: 'eventLabel' : 'display',
        EXPECTED: 'eventNonInteraction' : true
        EXPECTED: });
        """
        pass

    def test_003_tap_on_the_links_inside_the_cookie_bannerprivacy_policy_then_cookie_policytype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on the links inside the cookie banner:"Privacy policy'' then ''Cookie policy"
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter
        EXPECTED: The following events with corresponding parameters is present in data layer:
        EXPECTED: * For Privacy policy:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'cookie',
        EXPECTED: 'eventLabel' : 'privacy policy'
        EXPECTED: });
        EXPECTED: * For Cookie policy:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'cookie',
        EXPECTED: 'eventLabel' : 'cookie policy'
        EXPECTED: });
        """
        pass

    def test_004_tap_accept_on_cookie_banner(self):
        """
        DESCRIPTION: Tap "Accept" on Cookie banner
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'cookie',
        EXPECTED: 'eventLabel' : 'accept'
        EXPECTED: });
        """
        pass

    def test_005_clear_cache_and_log_in_with_an_active_opt_in_user_so_that_active_opt_in_updated_policy_banner_is_shown_together_with_cookie_banner(self):
        """
        DESCRIPTION: Clear cache and log in with an active opt-in user so that active opt-in updated policy banner is shown together with Cookie banner
        EXPECTED: Active opt-in updated privacy policy banner is shown above Cookie policy banner
        """
        pass

    def test_006_tap_on_the_my_account_link_inside_the_active_opt_in_bannertype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on the "My Account "link inside the active opt-in banner.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: {
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'active opt-in',
        EXPECTED: 'eventLabel' : 'my account'
        EXPECTED: }
        """
        pass

    def test_007_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat Steps 3-4
        EXPECTED: Idem
        """
        pass

    def test_008_clear_cache_and_log_in_with_an_inactive_opt_in_user_so_that_inactive_opt_in_updated_policy_banner_is_shown_together_with_cookie_banner(self):
        """
        DESCRIPTION: Clear cache and log in with an inactive opt-in user so that inactive opt-in updated policy banner is shown together with Cookie banner
        EXPECTED: Inactive opt-in updated privacy policy banner is shown above Cookie policy banner
        """
        pass

    def test_009_tap_on_market_preferences_link_inside_the_inactive_opt_in_bannertype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on "Market Preferences" link inside the inactive opt-in banner.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: {
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'inactive opt-in',
        EXPECTED: 'eventLabel' : 'marketing preferences'
        EXPECTED: }
        """
        pass

    def test_010_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat Steps 3-4
        EXPECTED: Idem
        """
        pass

    def test_011_clear_cache_and_log_in_with_an_opt_out_user_so_that_opt_out_updated_policy_banner_is_shown_together_with_cookie_banner(self):
        """
        DESCRIPTION: Clear cache and log in with an opt-out user so that opt-out updated policy banner is shown together with Cookie banner
        EXPECTED: Opt-out updated privacy policy banner is shown above Cookie policy banner
        """
        pass

    def test_012_tap_on_the_my_account_link_inside_the_active_opt_out_bannertype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on the "My Account "link inside the active opt-out banner.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: {
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'active opt-out',
        EXPECTED: 'eventLabel' : 'my account'
        EXPECTED: }
        """
        pass

    def test_013_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat Steps 3-4
        EXPECTED: Idem
        """
        pass
