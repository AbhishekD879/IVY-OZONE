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
class Test_C363808_Tracking_of_International_Tote_Clear_Betslip_button(Common):
    """
    TR_ID: C363808
    NAME: Tracking of International Tote 'Clear Betslip' button
    DESCRIPTION: This Test Case verifies tracking in the Google Analytic's data Layer due user clicks on  'Clear Betslip' on the International Tote Event Details page.
    DESCRIPTION: **Jira ticket**
    DESCRIPTION: * BMA-19374 International Tote: Google Analytics Tracking
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_the_international_tote_event_details_page(self):
        """
        DESCRIPTION: Navigate to the International Tote Event Details page
        EXPECTED: International Tote Event Details page is opened
        """
        pass

    def test_003_enter_value_to_the_stake_field(self):
        """
        DESCRIPTION: Enter value to the 'Stake' field
        EXPECTED: Entered value is shown in the 'Stake' field
        """
        pass

    def test_004_click_on_clear_betslip_button(self):
        """
        DESCRIPTION: Click on 'Clear Betslip' button
        EXPECTED: Entered value is cleared from the 'Stake' field
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'clear betslip click',
        EXPECTED: });
        """
        pass

    def test_006_repeat_steps_2_5_for_pool_types_win_place_show_exacta_trifecta(self):
        """
        DESCRIPTION: Repeat steps 2-5 for pool types:
        DESCRIPTION: * Win
        DESCRIPTION: * Place
        DESCRIPTION: * Show
        DESCRIPTION: * Exacta
        DESCRIPTION: * Trifecta
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_1_6_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-6 for Logged In user
        EXPECTED: 
        """
        pass
