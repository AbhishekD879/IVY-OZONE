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
class Test_C814129_Tracking_of_selecting_Quick_Stake_buttons(Common):
    """
    TR_ID: C814129
    NAME: Tracking of selecting Quick Stake buttons
    DESCRIPTION: This test case verifies selecting Quick Stake buttons
    PRECONDITIONS: * Test case should be run on Mobile Only
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: AUTOTEST: [C1288418]
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_sportrace_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/<Race> selection to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        pass

    def test_003_tap_pluscurrency_symbol5_button(self):
        """
        DESCRIPTION: Tap '+<currency symbol>5' button
        EXPECTED: Value of 5 is added to 'Stake' field
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'quick stake',
        EXPECTED: 'eventLabel' : '5'
        EXPECTED: });
        """
        pass

    def test_005_repeat_steps_3_4_the_next_quick_stake_buttons_pluscurrency_symbol10_pluscurrency_symbol50_pluscurrency_symbol100note_that_for_sek_currency_the_values_of_quick_stakes_are_50_100_500_1000(self):
        """
        DESCRIPTION: Repeat steps #3-4 the next Quick Stake buttons
        DESCRIPTION: * '+<currency symbol>10'
        DESCRIPTION: * '+<currency symbol>50'
        DESCRIPTION: * '+<currency symbol>100'
        DESCRIPTION: **NOTE** that for SEK currency the values of quick stakes are: 50, 100, 500, 1000
        EXPECTED: 
        """
        pass

    def test_006_log_in_with_user_with_any_currency_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Log in with user with any currency and repeat steps #2-5
        EXPECTED: 
        """
        pass
