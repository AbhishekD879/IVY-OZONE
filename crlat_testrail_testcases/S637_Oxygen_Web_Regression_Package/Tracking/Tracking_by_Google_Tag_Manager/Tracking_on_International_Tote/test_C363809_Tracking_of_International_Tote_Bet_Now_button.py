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
class Test_C363809_Tracking_of_International_Tote_Bet_Now_button(Common):
    """
    TR_ID: C363809
    NAME: Tracking of International Tote 'Bet Now' button
    DESCRIPTION: This Test Case verifies tracking in the Google Analytic's data Layer due user clicks on  'Bet Now'  button on the International Tote Event Details page.
    DESCRIPTION: **Jira ticket**
    DESCRIPTION: * BMA-19374 International Tote: Google Analytics Tracking
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_the_international_tote_and_open_any_event_details_page(self):
        """
        DESCRIPTION: Navigate to the International Tote and open any Event Details page
        EXPECTED: * International Tote Event Details page is opened
        EXPECTED: * 'Bet Now' button is disabled
        """
        pass

    def test_003_enter_value_to_the_stake_field(self):
        """
        DESCRIPTION: Enter value to the 'Stake' field
        EXPECTED: * Entered value is shown in the 'Stake' field
        EXPECTED: * 'Bet Now' button becomes enabled
        """
        pass

    def test_004_click_on_bet_now_button(self):
        """
        DESCRIPTION: Click on 'Bet Now' button
        EXPECTED: * Bet has been placed successfully
        EXPECTED: * 'Bet Receipt' is shown
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'international tote',
        EXPECTED: 'eventAction' : 'stake entry click',
        EXPECTED: });
        """
        pass

    def test_006_click_on_continue_button_on_the_bet_receipt(self):
        """
        DESCRIPTION: Click on 'Continue' button on the Bet Receipt
        EXPECTED: * 'Bet Receipt' is disappeared
        EXPECTED: * International Tote Event Details page is opened
        """
        pass

    def test_007_trigger_an_error_message_for_outcome_and_click_on_bet_now_button(self):
        """
        DESCRIPTION: Trigger an error message for outcome and click on 'Bet Now' button
        EXPECTED: * Error message appears for particular outcome
        EXPECTED: * Bet is unsuccessful
        EXPECTED: * 'Bet Now' button is disabled
        """
        pass

    def test_008_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'international tote',
        EXPECTED: 'eventAction' : 'stake entry click',
        EXPECTED: });
        """
        pass

    def test_009_repeat_steps_7_8_for_error_message_for_unit_stake_error_messages_for_a_few_outcomes_few_unit_stake_error_message_for_total_stake(self):
        """
        DESCRIPTION: Repeat steps 7-8 for:
        DESCRIPTION: * Error message for 'Unit Stake'
        DESCRIPTION: * Error messages for a few outcomes (few 'Unit Stake')
        DESCRIPTION: * Error message for 'Total Stake'
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_2_5_for_pool_types_win_place_show_exacta_trifecta(self):
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
