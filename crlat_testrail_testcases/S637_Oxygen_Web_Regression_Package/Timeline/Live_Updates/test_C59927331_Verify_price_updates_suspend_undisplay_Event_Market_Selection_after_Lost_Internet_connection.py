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
class Test_C59927331_Verify_price_updates_suspend_undisplay_Event_Market_Selection_after_Lost_Internet_connection(Common):
    """
    TR_ID: C59927331
    NAME: Verify price updates, suspend/undisplay Event/Market/Selection after Lost Internet connection
    DESCRIPTION: This test case verifies price updates, suspend/undisplay Event/Market/Selection after Lost Internet connection
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Live Campaign is created
    PRECONDITIONS: 2.Timeline posts with prices are created and published
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_tap_on_timeline_bubblealadbrokes__ladbrokes_loungebuttonbcoral___coral_pulse_button(self):
        """
        DESCRIPTION: Tap on Timeline Bubble
        DESCRIPTION: a.Ladbrokes- 'Ladbrokes Lounge'button
        DESCRIPTION: b.Coral - 'Coral pulse' button
        EXPECTED: Page with the published post should be opened
        EXPECTED: -Content should be the same as in CMS
        EXPECTED: -In WS 'Post' response should be present with all fields from CMS
        """
        pass

    def test_002_trigger_situation_with_losing_connection(self):
        """
        DESCRIPTION: Trigger situation with losing connection
        EXPECTED: - Connection is interrupted
        """
        pass

    def test_003_navigate_to_the_ti_backoffice_and_change_price_for_the_selection_for_the_timeline_post(self):
        """
        DESCRIPTION: Navigate to the TI (backoffice) and **change price** for the selection for the Timeline Post
        EXPECTED: - Price is changed and saved for the selection in the TI (backoffice)
        """
        pass

    def test_004_back_to_device_after_recovering_connection_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Back to device after recovering connection and verify outcomes for the event
        EXPECTED: - Response with updates is received in WS
        EXPECTED: - Page doesn't reload
        EXPECTED: - Price is changed for Post in the Timeline:
        EXPECTED: - *Blue color if the price has decreased*
        EXPECTED: - *Red color if the price has increased*
        EXPECTED: ![](index.php?/attachments/get/119601720)
        """
        pass

    def test_005_trigger_situation_with_losing_connection(self):
        """
        DESCRIPTION: Trigger situation with losing connection
        EXPECTED: - Connection is interrupted
        """
        pass

    def test_006_navigate_to_the_ob_and_suspend_eventmarketselection_for_the_timeline_post(self):
        """
        DESCRIPTION: Navigate to the OB and **suspend** Event/Market/Selection for the Timeline Post
        EXPECTED: - Changes are saved successfully
        EXPECTED: - Event/Market/Selection is suspended
        """
        pass

    def test_007_back_to_device_after_recovering_connection_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Back to device after recovering connection and verify outcomes for the event
        EXPECTED: - Response with updates is received in WS
        EXPECTED: - Page doesn't reload
        EXPECTED: - Price/Odds button of this event is displayed as greyed out and become disabled and NOT displaying the prices
        EXPECTED: ![](index.php?/attachments/get/119601719)
        """
        pass

    def test_008_trigger_situation_with_losing_connection(self):
        """
        DESCRIPTION: Trigger situation with losing connection
        EXPECTED: - Connection is interrupted
        """
        pass

    def test_009_navigate_to_the_ti_backoffice_and_do_undisplay_eventmarketselection_for_the_timeline_post(self):
        """
        DESCRIPTION: Navigate to the TI (backoffice) and do **Undisplay** Event/Market/Selection for the Timeline Post
        EXPECTED: - Changes are saved successfully
        EXPECTED: - Event/Market/Selection is Disabled
        """
        pass

    def test_010_back_to_device_after_recovering_connection_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Back to device after recovering connection and verify outcomes for the event
        EXPECTED: - Response with updates is received in WS
        EXPECTED: - Page doesn't reload
        EXPECTED: - Corresponding 'Price/Odds' button displays with n/a status
        EXPECTED: ![](index.php?/attachments/get/119601968)
        """
        pass
