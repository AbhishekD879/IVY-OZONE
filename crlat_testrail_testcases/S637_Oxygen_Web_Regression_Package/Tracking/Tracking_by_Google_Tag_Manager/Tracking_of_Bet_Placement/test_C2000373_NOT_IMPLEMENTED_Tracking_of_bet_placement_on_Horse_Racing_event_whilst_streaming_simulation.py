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
class Test_C2000373_NOT_IMPLEMENTED_Tracking_of_bet_placement_on_Horse_Racing_event_whilst_streaming_simulation(Common):
    """
    TR_ID: C2000373
    NAME: [NOT IMPLEMENTED] Tracking of bet placement on Horse Racing event whilst streaming simulation
    DESCRIPTION: This test case verifies bet placement on Horse Racing event while streaming simulation
    DESCRIPTION: Should be covered on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: - Oxygen app is loaded > Home page is opened
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User has enough balance on his account
    PRECONDITIONS: - Horse Racing events with mapped visualization are available
    PRECONDITIONS: - Browser Console is opened
    """
    keep_browser_open = True

    def test_001_go_to_horse_racing__any_event_edp_from_uk__ire_group_that_has_more_than_5_minutes_before_event_is_started(self):
        """
        DESCRIPTION: Go to Horse Racing > any event EDP from 'UK & IRE' group that has more than 5 minutes before event is started
        EXPECTED: * 'Watch Free' button is inactive by default (there is more than 15 minutes before event is started)
        EXPECTED: * 'Watch Free' area is automatically expanded and video is launched (there is more than 5 minutes before event is started)
        """
        pass

    def test_002_tap_watch_free_button_if_there_is_more_than_15_minutes_before_event_is_started(self):
        """
        DESCRIPTION: Tap 'Watch Free' button (if there is more than 15 minutes before event is started)
        EXPECTED: Video is launched
        """
        pass

    def test_003_add_selections_to_quick_betbetslip(self):
        """
        DESCRIPTION: Add selection(s) to Quick Bet/Betslip
        EXPECTED: Selection(s) is(are) available within Quick Bet/Betslip
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and press 'Enter'
        EXPECTED: The following tracking record is available:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'add to betslip',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'categoryID' : '<< OPENBET CATEGORY ID >>',
        EXPECTED: 'typeID' : '<< OPENBET TYPE ID >>',
        EXPECTED: 'eventID' : '<< OPENBET EVENT ID >>',
        EXPECTED: 'selectionID' : '<< OPENBET SELECTION ID >>',
        EXPECTED: 'inPlayStatus' : '<< IN PLAY STATUS >>',
        EXPECTED: 'location' : '<< LOCATION >>',
        EXPECTED: 'customerBuilt' : '<< CUSTOMER BUILT >>',
        EXPECTED: 'streamActive' : '<< STREAM ACTIVE >>',{{}}
        EXPECTED: }}{{'streamID' : '<< STREAM ID >>'{{}}
        EXPECTED: });
        """
        pass

    def test_005_enter_valid_value_into_amount_field__tap_bet_now(self):
        """
        DESCRIPTION: Enter valid value into 'Amount' field > Tap 'Bet Now'
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and press 'Enter'
        EXPECTED: The following tracking record is available:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'betID' : '<< BET ID >>',
        EXPECTED: 'betType' : '<< BET TYPE >>',
        EXPECTED: 'betCategory' : '<< BET CATEGORY >>',
        EXPECTED: 'betInPlay' : '<< BET IN PLAY >>',
        EXPECTED: 'bonusBet' : '<< BONUS BET >>',
        EXPECTED: 'location' : '<< LOCATION >>',
        EXPECTED: 'customerBuilt' : '<< CUSTOMER BUILT >>',
        EXPECTED: 'streamActive' : '<< STREAM ACTIVE >>',
        EXPECTED: }}{{'streamID' : '<< STREAM ID >>'
        EXPECTED: });
        """
        pass

    def test_007__in_app_add_selections_to_quick_betbetslip_in_ob_ti_trigger_error_message_during_bet_placement_immediately_after_readbet_request_is_senteg_price_changesuspension_etc(self):
        """
        DESCRIPTION: * In app: Add selection(s) to Quick Bet/Betslip
        DESCRIPTION: * In OB TI: Trigger error message during bet placement immediately after 'readbet' request is sent
        DESCRIPTION: e.g.: price change/suspension etc.
        EXPECTED: Error message appears in the Betslip/Quick Bet
        """
        pass

    def test_008_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and press 'Enter'
        EXPECTED: The following tracking record is available:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'failure',
        EXPECTED: 'betID' : '<< BET ID >>',
        EXPECTED: 'betType' : '<< BET TYPE >>',
        EXPECTED: 'betCategory' : '<< BET CATEGORY >>',
        EXPECTED: 'betInPlay' : '<< BET IN PLAY >>',
        EXPECTED: 'bonusBet' : '<< BONUS BET >>',
        EXPECTED: 'location' : '<< LOCATION >>',
        EXPECTED: 'customerBuilt' : '<< CUSTOMER BUILT >>',
        EXPECTED: 'streamActive' : '<< STREAM ACTIVE >>',
        EXPECTED: }}{{'streamID' : '<< STREAM ID >>'
        EXPECTED: });
        """
        pass
