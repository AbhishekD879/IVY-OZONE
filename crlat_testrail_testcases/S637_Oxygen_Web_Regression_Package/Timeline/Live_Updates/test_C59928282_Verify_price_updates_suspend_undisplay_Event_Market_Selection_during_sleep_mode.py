import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.timeline
@vtest
class Test_C59928282_Verify_price_updates_suspend_undisplay_Event_Market_Selection_during_sleep_mode(Common):
    """
    TR_ID: C59928282
    NAME: Verify price updates, suspend/undisplay Event/Market/Selection during sleep mode
    DESCRIPTION: This test case Verifies price updates, suspend/undisplay Event/Market/Selection during sleep mode
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Live Campaign is created
    PRECONDITIONS: 2.Timeline posts with prices are created and published
    PRECONDITIONS: -Load the app
    PRECONDITIONS: -User is logged in ( NOTE Timeline is displayed ONLY for Logged In Users )
    PRECONDITIONS: -Navigate to the page with configured 'Timeline' (e.g./home/featured)
    PRECONDITIONS: It should be verified for:
    PRECONDITIONS: - Races
    PRECONDITIONS: - Tier 1 Sports
    PRECONDITIONS: - Tier 2 Sports
    PRECONDITIONS: - Tier 3 Sports
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_click_on_the_timeline_bubblealadbrokes_ladbrokes_lounge_buttonbcoral__coral_pulse_button(self):
        """
        DESCRIPTION: Click on the Timeline Bubble
        DESCRIPTION: a.Ladbrokes-'Ladbrokes Lounge' button
        DESCRIPTION: b.Coral- 'Coral Pulse' button
        EXPECTED: - Page with the published post is opened
        EXPECTED: - Price is present in the post
        EXPECTED: - Content is the same as in CMS
        EXPECTED: - In WS 'POST' response is present with all fields form CMS
        """
        pass

    def test_002_wait_until_the_application_will_be_into_sleep_mode(self):
        """
        DESCRIPTION: Wait until the application will be into sleep mode
        EXPECTED: The app is in the sleep mode
        """
        pass

    def test_003_navigate_to_the_ob_and_change_price_for_the_selection_for_the_timeline_post(self):
        """
        DESCRIPTION: Navigate to the OB and **change price** for the selection for the Timeline Post
        EXPECTED: Price is changed and saved for the selection
        """
        pass

    def test_004_open_the_app_and_click_on_the_ladbrokes_lounge_button_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Open the app and click on the 'Ladbrokes Lounge' button and verify outcomes for the event
        EXPECTED: - Corresponding 'Price/Odds' button displays the new price and it changes its color to:
        EXPECTED: Blue color if the price has decreased
        EXPECTED: Red color if the price has increased
        EXPECTED: ![](index.php?/attachments/get/119601720)
        """
        pass

    def test_005_wait_until_the_application_will_be_into_sleep_mode(self):
        """
        DESCRIPTION: Wait until the application will be into sleep mode
        EXPECTED: The app is in the sleep mode
        """
        pass

    def test_006_navigate_to_the_ob_and_suspend_eventmarketselection_for_the_timeline_post(self):
        """
        DESCRIPTION: Navigate to the OB and **suspend** Event/Market/Selection for the Timeline Post
        EXPECTED: - Changes are saved successfully
        EXPECTED: - Event/Market/Selection is suspended
        """
        pass

    def test_007_open_the_app_and_click_on_the_ladbrokes_lounge_button_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Open the app and click on the 'Ladbrokes Lounge' button and verify outcomes for the event
        EXPECTED: Price/Odds button of this event is displayed as greyed out and become disabled and NOT displaying the prices
        EXPECTED: ![](index.php?/attachments/get/119601719)
        """
        pass

    def test_008_wait_until_the_application_will_be_into_sleep_mode(self):
        """
        DESCRIPTION: Wait until the application will be into sleep mode
        EXPECTED: The app is in the sleep mode
        """
        pass

    def test_009_navigate_to_the_ob_and_do_active_eventmarketselection_for_the_timeline_post(self):
        """
        DESCRIPTION: Navigate to the OB and do **ACTIVE** Event/Market/Selection for the Timeline Post
        EXPECTED: - Changes are saved successfully
        EXPECTED: - Event/Market/Selection is active
        """
        pass

    def test_010_open_the_app_and_click_on_the_ladbrokes_lounge_button_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Open the app and click on the 'Ladbrokes Lounge' button and verify outcomes for the event
        EXPECTED: Corresponding 'Price/Odds' button is active and displays the old price
        """
        pass

    def test_011_wait_until_the_application_will_be_into_sleep_mode(self):
        """
        DESCRIPTION: Wait until the application will be into sleep mode
        EXPECTED: The app is in the sleep mode
        """
        pass

    def test_012_navigate_to_the_ob_and_undisplay_eventmarketselection_for_the_timeline_post(self):
        """
        DESCRIPTION: Navigate to the OB and **Undisplay** Event/Market/Selection for the Timeline Post
        EXPECTED: - Changes are saved successfully
        EXPECTED: - Event/Market/Selection is undisplayed
        """
        pass

    def test_013_open_the_app_and_click_on_the_ladbrokes_lounge_button_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Open the app and click on the 'Ladbrokes Lounge' button and verify outcomes for the event
        EXPECTED: Corresponding 'Price/Odds' button displays with n/a status
        EXPECTED: ![](index.php?/attachments/get/119601968)
        """
        pass

    def test_014_wait_until_the_application_will_be_into_sleep_mode(self):
        """
        DESCRIPTION: Wait until the application will be into sleep mode
        EXPECTED: The app is in the sleep mode
        """
        pass

    def test_015_navigate_to_the_ob_and_display_eventmarketselection_for_the_timeline_post(self):
        """
        DESCRIPTION: Navigate to the OB and **Display** Event/Market/Selection for the Timeline Post
        EXPECTED: - Changes are saved successfully
        EXPECTED: - Event/Market/Selection is displayed
        """
        pass

    def test_016_open_the_app_and_click_on_the_ladbrokes_lounge_button_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Open the app and click on the 'Ladbrokes Lounge' button and verify outcomes for the event
        EXPECTED: Corresponding 'Price/Odds' button displays the old price
        """
        pass
