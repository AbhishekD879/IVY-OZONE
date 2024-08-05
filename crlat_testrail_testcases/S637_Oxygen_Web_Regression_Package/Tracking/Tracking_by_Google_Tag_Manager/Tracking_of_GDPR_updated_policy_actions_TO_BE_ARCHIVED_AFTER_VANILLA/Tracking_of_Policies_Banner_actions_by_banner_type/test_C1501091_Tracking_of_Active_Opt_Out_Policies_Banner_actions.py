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
class Test_C1501091_Tracking_of_Active_Opt_Out_Policies_Banner_actions(Common):
    """
    TR_ID: C1501091
    NAME: Tracking of 'Active Opt Out' Policies Banner actions
    DESCRIPTION: This test case verifies GA tracking of 'Active Opt Out' Policies Banner actions.
    DESCRIPTION: Opt-Out banner = Updated privacy policy banner for opt-out user, a customer who has **opted out** (of all Marketing comms) during registration journey or in "My Account"
    PRECONDITIONS: 1.	Test Case should be executed on  mobile, tablet & desktop platforms
    PRECONDITIONS: 2.	Dev Tools -> Console should be opened
    PRECONDITIONS: 3.	Instruction for real mobile devices/ wrappers debugging: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: Given cookie banner is accepted by user.
    PRECONDITIONS: Instructions on how to trigger opt-out updated policy banner are detailed in TC [C1474610]
    PRECONDITIONS: **NOTE-Important**: For the URL links clicks (privacy and cookie policies links), the tracked **eventlabel value** in dataLayer will be based on the title attribute text in the respective banner’s CMS static block. Thus the eventLabel may change from the one recorded in current test case, in case the TitleID will be changed in the future in CMS. Always check this title in CMs before running the test case.
    """
    keep_browser_open = True

    def test_001_trigger_the_situation_when_opt_out_updated_policies_banner_is_shown(self):
        """
        DESCRIPTION: Trigger the situation when opt-out updated policies banner is shown
        EXPECTED: Opt-out updated privacy policy banner is shown
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'active opt-out',
        EXPECTED: 'eventLabel' : 'display',
        EXPECTED: 'eventNonInteraction' : true
        EXPECTED: });
        """
        pass

    def test_003_tap_on_the_links_inside_the_bannerprivacy_policy_then_cookie_policytype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on the links inside the banner:"Privacy policy'' then ''Cookie policy"
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following events with corresponding parameters is present in data layer:
        EXPECTED: * For Privacy policy:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'active opt-out',
        EXPECTED: 'eventLabel' : 'privacy policy'
        EXPECTED: });
        EXPECTED: * For Cookie policy:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'active opt-out',
        EXPECTED: 'eventLabel' : 'cookie policy'
        EXPECTED: });
        """
        pass

    def test_004_tap_on_my_account_link_inside_the_bannertype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on "My Account" link inside the banner.
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

    def test_005_tap_on_the_x_button_inside_updated_policy_bannertype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on the X button inside Updated policy banner
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'active opt-out',
        EXPECTED: 'eventLabel' : 'close'
        EXPECTED: });
        """
        pass
