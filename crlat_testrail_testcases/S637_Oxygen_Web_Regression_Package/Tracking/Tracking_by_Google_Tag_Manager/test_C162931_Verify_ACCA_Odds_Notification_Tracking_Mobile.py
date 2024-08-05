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
class Test_C162931_Verify_ACCA_Odds_Notification_Tracking_Mobile(Common):
    """
    TR_ID: C162931
    NAME: Verify ACCA Odds Notification Tracking (Mobile)
    DESCRIPTION: This test case verifies ACCA Odds Notification Tracking (Mobile)
    PRECONDITIONS: 1. Test Case should be executed on mobile devices
    PRECONDITIONS: 2. Dev Tools -> Console should be opened
    PRECONDITIONS: 3. Instruction for mobile devices debugging: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_sports_landing_page(self):
        """
        DESCRIPTION: Go to Sports Landing page
        EXPECTED: Sports Landing page is opened
        """
        pass

    def test_003_add_at_least_two_selections_from_different_events_to_the_betslip_where_potential_payout_parameter_is_equal_or_more_than_200(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip where potential payout parameter is equal or more than 2.00
        EXPECTED: * ACCA Odds Notification appears at the bottom of the screen but above Footer menu for Mobile
        """
        pass

    def test_004_tap_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Tap on ACCA Odds Notification message
        EXPECTED: * User is redirected to the Betslip
        EXPECTED: * Multiples are available in the Betslip
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventAction' : 'click ',
        EXPECTED: 'eventLabel' : 'odds notification banner'
        EXPECTED: });
        """
        pass

    def test_006_add_one_more_selection_from_another_event_to_the_betslip(self):
        """
        DESCRIPTION: Add one more selection from another event to the Betslip
        EXPECTED: * ACCA Odds Notification message is still displayed
        EXPECTED: * Multiples name on ACCA Odds Notification message is updated properly
        EXPECTED: * Odds is recalculated and new price is displayed
        """
        pass

    def test_007_tap_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Tap on ACCA Odds Notification message
        EXPECTED: * User is redirected to the Betslip
        EXPECTED: * Multiples are available in the Betslip
        """
        pass

    def test_008_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventAction' : 'click ',
        EXPECTED: 'eventLabel' : 'odds notification banner'
        EXPECTED: });
        """
        pass

    def test_009_repeat_steps_6_8_for_different_type_of_multiples(self):
        """
        DESCRIPTION: Repeat steps 6-8 for different type of multiples
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_2_8_for_races(self):
        """
        DESCRIPTION: Repeat steps 2-8 for Races
        EXPECTED: 
        """
        pass
