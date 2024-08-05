import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870370_Verify_GDPR_banner(Common):
    """
    TR_ID: C44870370
    NAME: Verify GDPR banner
    DESCRIPTION: Verify GDPR banner- Text and functionality
    DESCRIPTION: "Updated Policies
    DESCRIPTION: We’ve updated our Privacy Policy and Cookie Policy to provide more detailed information as requested by new EU privacy laws."
    PRECONDITIONS: C&C cleared.
    """
    keep_browser_open = True

    def test_001_user_loads_the_ladbrokes_siteappverify_that_on_load_the_gdpr_banner_is_displayed__text_to_be_displayedupdated_policies_bold_bigger_fontweve_updated_our_privacy_policy_and_cookie_policy_to_provide_more_detailed_information_as_requested_by_new_eu_privacy_laws_privacy_policy_cookie_policy_in_bold__accept_text_on_accept_button__when_user_tapclick_on_accept_button_the_banner_disappears(self):
        """
        DESCRIPTION: User loads the Ladbrokes site/app
        DESCRIPTION: Verify that on load, the GDPR banner is displayed
        DESCRIPTION: - Text to be displayed:
        DESCRIPTION: "Updated Policies" (bold, bigger font)
        DESCRIPTION: "We’ve updated our Privacy Policy and Cookie Policy to provide more detailed information as requested by new EU privacy laws." (Privacy Policy, Cookie Policy in bold)
        DESCRIPTION: - "ACCEPT" text on Accept button
        DESCRIPTION: - When user tap/click on accept button, the banner disappears
        EXPECTED: GDPR Banner is displayed as per GDs and works fine
        """
        pass

    def test_002_close_the_browser_kill_the_appload_again_the_ladbrokes_siteapp_and_check_if_the_gdpr_banner_is_displayed(self):
        """
        DESCRIPTION: Close the browser/ kill the app
        DESCRIPTION: Load again the Ladbrokes site/app and check if the GDPR Banner is displayed
        EXPECTED: GDPR Banner should not be displayed displayed
        """
        pass

    def test_003_close_the_browser_kill_the_appclear_ccload_again_the_ladbrokes_siteapp_and_check_if_the_gdpr_banner_is_displayedlog_in_on_site_and_observe_if_the_functionality_is_the_same_as_on_step_1check_that_after_banner_disappears_user_is_logged_in(self):
        """
        DESCRIPTION: Close the browser/ kill the app
        DESCRIPTION: Clear C&C
        DESCRIPTION: Load again the Ladbrokes site/app and check if the GDPR Banner is displayed
        DESCRIPTION: Log in on site and observe if the functionality is the same as on step 1
        DESCRIPTION: Check that after banner disappears, user is logged in
        EXPECTED: GDPR Banner is displayed as per GDs and works fine regardless user is logged out or logged in
        """
        pass
