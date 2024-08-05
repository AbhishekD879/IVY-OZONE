import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.timeline
@vtest
class Test_C60018038_Tracking_of_toggle_ON_toggle_OFF(Common):
    """
    TR_ID: C60018038
    NAME: Tracking of toggle ON/ toggle OFF
    DESCRIPTION: This test case verifies GA tracking of toggle ON/ toggle OFF for Timeline in the User's Settings
    PRECONDITIONS: Timeline is turn ON in the CMS
    PRECONDITIONS: Log in to the app
    """
    keep_browser_open = True

    def test_001_go_to_account_setting_on_ui_indexphpattachmentsget121567982__settings___betting_settings___ladbrokes_lounge_sectionuntick_the_checkbox_and_save_the_changes(self):
        """
        DESCRIPTION: Go to Account Setting on UI ![](index.php?/attachments/get/121567982)
        DESCRIPTION: -> 'Settings' -> 'Betting Settings' -> 'Ladbrokes Lounge' section
        DESCRIPTION: Untick the checkbox and save the changes
        EXPECTED: - Checkbox is unticked
        EXPECTED: - Changes are saved successfully
        """
        pass

    def test_002_navigate_to_the_page_with_timeline_configured_and_verify_timeline_displaying(self):
        """
        DESCRIPTION: Navigate to the page with Timeline configured and verify 'Timeline' displaying
        EXPECTED: - 'Timeline' is NOT displayed at the bottom of the page (above the footer menu) for the setup Page Urls (CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field)
        """
        pass

    def test_003_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: - ‘event’ : ‘trackEvent’,
        EXPECTED: - ‘eventCategory’ : ‘betting settings’,
        EXPECTED: - ‘eventAction’ : ‘ladbrokes lounge’,
        EXPECTED: - ‘eventLabel’: 'toggle off'
        """
        pass

    def test_004_return_to_users_settings_tick_the_checkbox_and_save_the_changes(self):
        """
        DESCRIPTION: Return to User's Settings, tick the checkbox and save the changes
        EXPECTED: - Checkbox is ticked
        EXPECTED: - Changes are saved successfully
        """
        pass

    def test_005_navigate_to_the_page_with_timeline_configured_and_verify_timeline_displayingtype_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Navigate to the page with Timeline configured and verify 'Timeline' displaying
        DESCRIPTION: Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: - 'Timeline' is displayed at the bottom of the page (above the footer menu) for the setup Page
        EXPECTED: - The following parameters and values are present in 'dataLayer' object:
        EXPECTED: - ‘event’ : ‘trackEvent’,
        EXPECTED: - ‘eventCategory’ : ‘betting settings’,
        EXPECTED: - ‘eventAction’ : ‘ladbrokes lounge’,
        EXPECTED: - ‘eventLabel’: ‘toggle on'
        """
        pass
