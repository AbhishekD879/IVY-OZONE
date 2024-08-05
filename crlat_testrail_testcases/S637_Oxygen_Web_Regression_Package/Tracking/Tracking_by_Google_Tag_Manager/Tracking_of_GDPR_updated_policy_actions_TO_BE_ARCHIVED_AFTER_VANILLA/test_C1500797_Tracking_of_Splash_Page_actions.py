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
class Test_C1500797_Tracking_of_Splash_Page_actions(Common):
    """
    TR_ID: C1500797
    NAME: Tracking of Splash Page actions
    DESCRIPTION: This test case verifies GA tracking of Splash Page related actions.
    PRECONDITIONS: 1.	Test Case should be executed on  mobile, tablet & desktop platforms
    PRECONDITIONS: 2.	Dev Tools -> Console should be opened
    PRECONDITIONS: 3.	Instruction for real mobile devices/ wrappers debugging: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: Splash Page is shown to user in following scenarios:
    PRECONDITIONS: - when the user taps Complete Registration in the Account details page of the registration journey [REMOVED flow]
    PRECONDITIONS: - after closing inactive opt-in banner, where the user can choose whether user wants to set his marketing preferences. Instructions on how to trigger inactive opt-in updated policy banner are detailed in TC [C1474025]
    """
    keep_browser_open = True

    def test_001_removed_flow_steps_1_5_load_app_and_proceed_with_registering_a_new_user_with_valid_dataon_last_step_tap_complete_registration_in_the_account_details_page(self):
        """
        DESCRIPTION: [REMOVED flow: steps 1-5] Load app and proceed with registering a new user with valid data.
        DESCRIPTION: On last step tap Complete Registration in the Account details page.
        EXPECTED: User is successfully registered and  Opt-in Splash Page is shown.
        """
        pass

    def test_002_tap_on_the_links_in_the_footer_of_pageprivacy_policy_then_cookie_policytype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on the links in the footer of page:"Privacy policy'' then ''Cookie policy"
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter
        EXPECTED: The following events with corresponding parameters is present in data layer:
        EXPECTED: * For Privacy policy:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'splash',
        EXPECTED: 'eventAction' : 'link',
        EXPECTED: 'eventLabel' : 'privacy policy'
        EXPECTED: });
        EXPECTED: * For Cookie policy:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'splash',
        EXPECTED: 'eventAction' : 'link',
        EXPECTED: 'eventLabel' : 'cookie policy'
        EXPECTED: });
        """
        pass

    def test_003_tap_opt_in_button_on_splash_pagetype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap "OPT IN" button on Splash Page
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'splash',
        EXPECTED: 'eventAction' : 'opt in'
        EXPECTED: });
        """
        pass

    def test_004_repeat_step_1(self):
        """
        DESCRIPTION: Repeat Step 1
        EXPECTED: --
        """
        pass

    def test_005_tap_no_thanks_button_on_splash_pagetype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap "No Thanks" button on Splash Page
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'splash',
        EXPECTED: 'eventAction' : 'decline'
        EXPECTED: });
        """
        pass

    def test_006_log_in_with_an_inactive_opt_in_user_and_tap_x_button_to_close_the_updated_policy_banner(self):
        """
        DESCRIPTION: Log in with an inactive opt-in user and tap 'X' button to close the updated policy banner
        EXPECTED: Opt-in Splash Page is shown.
        """
        pass

    def test_007_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat Steps 2-3
        EXPECTED: --
        """
        pass

    def test_008_repeat_step_6(self):
        """
        DESCRIPTION: Repeat Step 6
        EXPECTED: --
        """
        pass

    def test_009_repeat_step_5(self):
        """
        DESCRIPTION: Repeat Step 5
        EXPECTED: --
        """
        pass
