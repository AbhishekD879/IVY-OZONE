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
class Test_C2000372_TO_UPDATE_Tracking_of_bet_placement_on_Racing_events_while_streaming(Common):
    """
    TR_ID: C2000372
    NAME: TO UPDATE Tracking of bet placement on <Racing> events while streaming
    DESCRIPTION: This test case verifies bet placement on <Racing> events while streaming
    DESCRIPTION: Should be covered for all available streaming types: IGMedia, ATR, RUK
    DESCRIPTION: Should be covered on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: - Oxygen app is loaded > Home page is opened
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User has enough balance on his account
    PRECONDITIONS: - <Racing> events with mapped streams (IGMedia, ATR, RUK) are available
    PRECONDITIONS: - In order to place a bet on <Racing> event while streaming, there should be less than 3 minutes before event is started
    PRECONDITIONS: - Browser Console is opened
    """
    keep_browser_open = True

    def test_001_navigate_to_any_racing_edp_with_available_streaming_has_streaming_icon_that_is_about_to_start(self):
        """
        DESCRIPTION: Navigate to any <Racing> EDP with available streaming (has 'streaming' icon) that is about to start
        EXPECTED: Corresponding <Racing> EDP is opened
        """
        pass

    def test_002_place_a_bet__1_gpb_to_qualify_for_stream_watching(self):
        """
        DESCRIPTION: Place a bet (>= 1 GPB) to qualify for stream watching
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_003_tap_live_stream_button_3_minutes_before_event_is_started(self):
        """
        DESCRIPTION: Tap 'Live Stream' button (3 minutes before event is started)
        EXPECTED: Stream is playing
        """
        pass

    def test_004_add_selections_to_quick_betbetslip(self):
        """
        DESCRIPTION: Add selection(s) to Quick Bet/Betslip
        EXPECTED: Selection(s) is(are) available within Quick Bet/Betslip
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_press_enter(self):
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
        EXPECTED: 'betInPlay' : '<< BET IN PLAY >>', e.g. yes/no
        EXPECTED: 'location' : '<< LOCATION >>', e.g. /football/event/{eventID}
        EXPECTED: 'customerBuilt' : '<< CUSTOMER BUILT >>', e.g. "no" (for all non YourCall bets)
        EXPECTED: 'streamActive' : '<< STREAM ACTIVE >>',{{}} e.g. true or false
        EXPECTED: }}{{'streamID' : '<< STREAM ID >>' e.g. {id} or "null" if id is not known{{}}
        EXPECTED: });
        EXPECTED: NOTE: For IGMedia 'streamActive'=null (as this data is not available in BE MS)
        """
        pass

    def test_006_enter_valid_value_into_amount_field__tap_bet_now(self):
        """
        DESCRIPTION: Enter valid value into 'Amount' field > Tap 'Bet Now'
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_press_enter(self):
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
        EXPECTED: 'inPlayStatus' : '<< IN PLAY STATUS >>', e.g. In Play, Pre Match
        EXPECTED: 'bonusBet' : '<< BONUS BET >>',
        EXPECTED: 'location' : '<< LOCATION >>', e.g. /football/event/{eventID}
        EXPECTED: 'customerBuilt' : '<< CUSTOMER BUILT >>', e.g. "no" (for all non YourCall bets)
        EXPECTED: 'streamActive' : '<< STREAM ACTIVE >>',{{}} e.g. true or false
        EXPECTED: }}{{'streamID' : '<< STREAM ID >> e.g. {id} or "null" if id is not known'
        EXPECTED: });
        EXPECTED: NOTE: For IGMedia 'streamActive'=null (as this data is not available in BE MS)
        """
        pass

    def test_008__in_app_add_selections_to_quick_betbetslip_in_ob_ti_trigger_error_message_during_bet_placement_immediately_after_readbet_request_is_senteg_price_changesuspension_etc(self):
        """
        DESCRIPTION: * In app: Add selection(s) to Quick Bet/Betslip
        DESCRIPTION: * In OB TI: Trigger error message during bet placement immediately after 'readbet' request is sent
        DESCRIPTION: e.g.: price change/suspension etc.
        EXPECTED: Error message appears in the Betslip/Quick Bet
        """
        pass

    def test_009_type_in_browser_console_datalayer_and_press_enter(self):
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
        EXPECTED: 'betInPlay' : '<< BET IN PLAY >>', e.g. yes/no
        EXPECTED: 'bonusBet' : '<< BONUS BET >>',
        EXPECTED: 'location' : '<< LOCATION >>', e.g. /football/event/{eventID}
        EXPECTED: 'customerBuilt' : '<< CUSTOMER BUILT >>', e.g. "no" (for all non YourCall bets)
        EXPECTED: 'streamActive' : '<< STREAM ACTIVE >>',{{}} e.g. true or false
        EXPECTED: }}{{'streamID' : '<< STREAM ID >>' e.g. {id} or "null" if id is not known
        EXPECTED: });
        EXPECTED: NOTE: For IGMedia 'streamActive'=null (as this data is not available in BE MS)
        """
        pass
