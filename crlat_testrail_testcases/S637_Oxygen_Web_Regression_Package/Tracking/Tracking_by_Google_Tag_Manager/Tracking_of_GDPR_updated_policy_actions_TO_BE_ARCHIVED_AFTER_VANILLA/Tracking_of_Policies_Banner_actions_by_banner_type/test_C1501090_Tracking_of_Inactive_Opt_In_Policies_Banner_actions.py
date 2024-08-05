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
class Test_C1501090_Tracking_of_Inactive_Opt_In_Policies_Banner_actions(Common):
    """
    TR_ID: C1501090
    NAME: Tracking of 'Inactive Opt In' Policies Banner actions
    DESCRIPTION: This test case verifies GA tracking of 'Inactive Opt In'  Policies Banner actions.
    DESCRIPTION: Inactive Opt-In banner = Updated privacy policy banner seen by the user who has “opted-in” via a pre-ticked box during registration and is **inactive customer**  (has not deposited or placed a bet in the last 13 months OR have not interacted with marketing in the last 12 months)
    PRECONDITIONS: 1.	Test Case should be executed on  mobile, tablet & desktop platforms
    PRECONDITIONS: 2.	Dev Tools -> Console should be opened
    PRECONDITIONS: 3.	Instruction for real mobile devices/ wrappers debugging: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: Given cookie banner is accepted by user.
    PRECONDITIONS: Instructions on how to trigger inactive opt-in updated policy banner are detailed in TC [C1474025]
    PRECONDITIONS: **NOTE-Important**: For the URL links clicks (privacy and cookie policies links), the tracked **eventlabel value** in dataLayer will be based on the title attribute text in the respective banner’s CMS static block. Thus the eventLabel may change from the one recorded in current test case, in case the TitleID will be changed in the future in CMS. Always check this title in CMs before running the test case.
    """
    keep_browser_open = True

    def test_001_trigger_the_situation_when_inactive_opt_in_updated_policy_banner_is_shown(self):
        """
        DESCRIPTION: Trigger the situation when inactive opt-in updated policy banner is shown
        EXPECTED: Inactive opt-in updated policy banner is displayed
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'inactive opt-in',
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
        EXPECTED: 'eventAction' : 'inactive opt-in',
        EXPECTED: 'eventLabel' : 'privacy policy'
        EXPECTED: });
        EXPECTED: * For Cookie policy:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : ‘inactive opt-in’,
        EXPECTED: 'eventLabel' : 'cookie policy'
        EXPECTED: });
        """
        pass

    def test_004_trigger_the_situation_when_inactive_opt_in_updated_policies_banner_is_showntap_on_the_check_box_next_to_the_bottom_text_area(self):
        """
        DESCRIPTION: Trigger the situation when inactive opt-in updated policies banner is shown.
        DESCRIPTION: Tap on the check box next to the bottom text area
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'inactive opt-in',
        EXPECTED: 'eventLabel' : 'opt in'
        EXPECTED: });
        """
        pass

    def test_005_trigger_the_situation_when_inactive_opt_in_updated_policies_banner_is_showntap_on_manage_my_preferences_link_inside_the_banner(self):
        """
        DESCRIPTION: Trigger the situation when inactive opt-in updated policies banner is shown.
        DESCRIPTION: Tap on "Manage my Preferences" link inside the banner
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: {
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'inactive opt-in',
        EXPECTED: 'eventLabel' : 'marketing preferences'
        EXPECTED: }
        """
        pass

    def test_006_tap_on_the_x_button_inside_updated_policy_bannertype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on the X button inside Updated policy banner
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'policies banner',
        EXPECTED: 'eventAction' : 'inactive opt-in',
        EXPECTED: 'eventLabel' : 'close'
        EXPECTED: });
        """
        pass
