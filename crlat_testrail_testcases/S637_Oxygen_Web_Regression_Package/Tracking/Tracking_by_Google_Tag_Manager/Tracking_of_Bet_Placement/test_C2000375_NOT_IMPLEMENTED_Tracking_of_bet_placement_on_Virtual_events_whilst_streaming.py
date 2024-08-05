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
class Test_C2000375_NOT_IMPLEMENTED_Tracking_of_bet_placement_on_Virtual_events_whilst_streaming(Common):
    """
    TR_ID: C2000375
    NAME: [NOT IMPLEMENTED] Tracking of bet placement on Virtual events whilst streaming
    DESCRIPTION: This test case verifies bet placement on Inspired Virtual Sports & Bet Radar Virtual Tournament events while streaming
    DESCRIPTION: Should be covered on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: - Oxygen app is loaded > Home page is opened
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User has enough balance on his account
    PRECONDITIONS: - Browser Console is opened
    """
    keep_browser_open = True

    def test_001_go_to_inspired_virtual_sportsracing(self):
        """
        DESCRIPTION: Go to Inspired Virtual <Sports>/<Racing>
        EXPECTED: Inspired Virtuals <Sport>/<Race> page is opened
        """
        pass

    def test_002_tap_on_play_button_within_the_video_stream(self):
        """
        DESCRIPTION: Tap on 'Play' button within the video stream
        EXPECTED: Video is playing
        """
        pass

    def test_003_add_any_sport_or_race_selection_to_quick_betbetslip(self):
        """
        DESCRIPTION: Add any <Sport> or <Race> selection to Quick Bet/Betslip
        EXPECTED: Inspired Virtuals <Sport> or <Race> selection is displayed within Quick Bet/Betslip
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

    def test_007__in_app_add_selections_to_quick_betbetslip_in_ob_ti_trigger_error_message_during_bet_placement_immediately_after_placebet_request_is_senteg_price_changesuspension_etc(self):
        """
        DESCRIPTION: * In app: Add selection(s) to Quick Bet/Betslip
        DESCRIPTION: * In OB TI: Trigger error message during bet placement immediately after 'placebet' request is sent
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

    def test_009_go_to_any_betradar_virtual_tournament_sport_tab__repeat_steps_2_8(self):
        """
        DESCRIPTION: Go to any BetRadar Virtual Tournament <Sport> tab & repeat steps 2-8
        EXPECTED: 
        """
        pass
