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
class Test_C1500800_Tracking_of_Marketing_Preferences_actions(Common):
    """
    TR_ID: C1500800
    NAME: Tracking of Marketing Preferences actions
    DESCRIPTION: This test case verifies GA tracking of 'Marketing Preferences' page actions.
    PRECONDITIONS: 1.	Test Case should be executed on  mobile, tablet & desktop platforms
    PRECONDITIONS: 2.	Dev Tools -> Console should be opened
    PRECONDITIONS: 3.	Instruction for real mobile devices/ wrappers debugging: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: Marketing Pref page is shown to logged in user in following scenarios:
    PRECONDITIONS: - when the user taps Complete Registration in the Account details page of the registration journey, and Splash Page with opt-in option is shown
    PRECONDITIONS: - after closing inactive opt-in banner, where the user can choose whether user wants to set his marketing preferences. Instructions on how to trigger inactive opt-in updated policy banner are detailed in TC [C1474025]
    PRECONDITIONS: - active opt-in banner> user is redirected to MP page when tapping My Preferences
    PRECONDITIONS: - inactive opt-in banner> user is redirected to MP page when ticking the Opt-in box
    PRECONDITIONS: - logged in user navigates at any time to MP page to submit marketing preferences changes
    """
    keep_browser_open = True

    def test_001_trigger_the_situation_when_marketing_preferences_page_is_shown_to_logged_in_user(self):
        """
        DESCRIPTION: Trigger the situation when Marketing Preferences page is shown to logged in user
        EXPECTED: Marketing Preferences page is displayed.
        """
        pass

    def test_002_in_preferences_top_section_de_select_default_alltype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: In Preferences top section de-select default 'All'
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'deselect',
        EXPECTED: 'eventLabel' : 'all'
        EXPECTED: });
        """
        pass

    def test_003_select_email_post_sms_phonetype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Select Email, Post, SMS, Phone
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following events with corresponding parameters are present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'select',
        EXPECTED: 'eventLabel' : 'email'
        EXPECTED: });
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'select',
        EXPECTED: 'eventLabel' : 'directMail'
        EXPECTED: });
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'select',
        EXPECTED: 'eventLabel' : 'SMS'
        EXPECTED: });
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'select',
        EXPECTED: 'eventLabel' : 'phone'
        EXPECTED: });
        """
        pass

    def test_004_in_preferences_top_section_de_select_again_alltype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: In Preferences top section de-select again 'All'
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'deselect',
        EXPECTED: 'eventLabel' : 'all'
        EXPECTED: });
        """
        pass

    def test_005_in_preferences_top_section_select__alltype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: In Preferences top section select  'All'
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'select',
        EXPECTED: 'eventLabel' : 'all'
        EXPECTED: });
        """
        pass

    def test_006_in_preferences_top_section_de_select_one_by_one_email_post_sms_phonetype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: In Preferences top section de-select one by one Email, Post, SMS, Phone
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following events with corresponding parameters are present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'deselect',
        EXPECTED: 'eventLabel' : 'email'
        EXPECTED: });
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'deselect',
        EXPECTED: 'eventLabel' : 'directMail'
        EXPECTED: });
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'deselect',
        EXPECTED: 'eventLabel' : 'SMS'
        EXPECTED: });
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'deselect',
        EXPECTED: 'eventLabel' : 'phone'
        EXPECTED: });
        """
        pass

    def test_007_tap_submit_on_marketing_preferences_pagetype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap 'Submit' on Marketing Preferences page
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'submit'
        EXPECTED: });
        """
        pass

    def test_008_tap_the_privacy_policy_and_the_cookie_policy_in_the_bottom_of_marketing_preferences_pagetype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap the privacy policy and the cookie policy in the bottom of Marketing Preferences page
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following events with corresponding parameters are present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'link',
        EXPECTED: 'eventLabel' : 'privacy policy'
        EXPECTED: });
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'marketing preferences',
        EXPECTED: 'eventAction' : 'link',
        EXPECTED: 'eventLabel' : 'cookie policy'
        EXPECTED: });
        """
        pass
