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
class Test_C863021_Tracking_of_unsuccessful_bet_placement(Common):
    """
    TR_ID: C863021
    NAME: Tracking of unsuccessful bet placement
    DESCRIPTION: This test case verifies tracking of unsuccessful bet placement
    PRECONDITIONS: * Test case should be run on Mobile Only
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * To view response open Dev tools -> Network -> WS -> choose the last request
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Attribute <<CUSTOMER BUILT>> show Yes/No,
    PRECONDITIONS: if bet type = "Build Your Bet shows 'Yes'
    PRECONDITIONS: **New Quickbet tracking parameters:** https://confluence.egalacoral.com/pages/viewpage.action?pageId=91470520
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: * Selected price/odds are highlighted in green
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_003_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: * 'Stake' field is populated with entered value
        """
        pass

    def test_004__tap_place_bet_button_trigger_situation_when_bpp_token_is_wrong_or_expired(self):
        """
        DESCRIPTION: * Tap 'PLACE BET' button
        DESCRIPTION: * Trigger situation when BPP token is wrong or expired
        EXPECTED: * Bet is NOT placed
        EXPECTED: * Error message is displayed on red background below 'QUICK BET' header
        """
        pass

    def test_005_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'failure',
        EXPECTED: 'errorMessage' : '<< ERROR MESSAGE >>',
        EXPECTED: 'errorCode' : '<< ERROR CODE >>',
        EXPECTED: 'betType' : 'Single',
        EXPECTED: 'betCategory' : '<< BET CATEGORY >>',
        EXPECTED: 'betInPlay' : '<< BET IN PLAY >>',
        EXPECTED: 'bonusBet' : '<< BONUS BET >>'
        EXPECTED: 'location' : '<< LOCATION >>',
        EXPECTED: 'customerBuilt' : '<< CUSTOMER BUILT >>'
        EXPECTED: });
        """
        pass

    def test_006_verify_errormessage_parameter(self):
        """
        DESCRIPTION: Verify **'errorMessage'** parameter
        EXPECTED: * **'errorMessage'** parameter corresponds to message displayed to user
        """
        pass

    def test_007_verify_errorcode_parameter(self):
        """
        DESCRIPTION: Verify **'errorCode'** parameter
        EXPECTED: * **'errorCode'** parameter corresponds to **error.code** value recieved in 31012 response in WS
        EXPECTED: * **'errorCode'** attribute is displayed in lower case
        """
        pass

    def test_008_verify_betcategory_parameter(self):
        """
        DESCRIPTION: Verify **'betCategory'** parameter
        EXPECTED: * **'betCategory'** parameter corresponds to OB category for particular <Sport> / <Race>
        """
        pass

    def test_009_verify_betinplay_parameter(self):
        """
        DESCRIPTION: Verify **'betInPlay'** parameter
        EXPECTED: * **'bonusBet'** = 'Yes' if user tried to place a bet on selection from Live event
        EXPECTED: * **'bonusBet'** = 'No' if user tried to place a bet on selection from Pre Match event
        """
        pass

    def test_010_verify_bonusbet_parameter(self):
        """
        DESCRIPTION: Verify **'bonusBet'** parameter
        EXPECTED: * **'bonusBet'** = 'True' if user tried to place a bet with free bet
        EXPECTED: * **'bonusBet'** = 'False' if user tried to place a bet without free bet
        """
        pass

    def test_011__tap_place_bet_button_trigger_situation_when_incorrectunparsable_price_is_sent_to_place_a_bet_repeat_steps_5_7(self):
        """
        DESCRIPTION: * Tap 'PLACE BET' button
        DESCRIPTION: * Trigger situation when incorrect/unparsable price is sent to place a bet
        DESCRIPTION: * Repeat steps #5-7
        EXPECTED: 
        """
        pass

    def test_012__tap_place_bet_button_trigger_situation_when_bpp_returns_internal_error_repeat_steps_5_7(self):
        """
        DESCRIPTION: * Tap 'PLACE BET' button
        DESCRIPTION: * Trigger situation when BPP returns internal error
        DESCRIPTION: * Repeat steps #5-7
        EXPECTED: 
        """
        pass

    def test_013__tap_place_bet_button_trigger_situation_when_error_returned_from_ob_in_case_when_user_places_a_bet_with_outdated_price_repeat_steps_5_7(self):
        """
        DESCRIPTION: * Tap 'PLACE BET' button
        DESCRIPTION: * Trigger situation when error returned from OB in case when user places a bet with outdated price
        DESCRIPTION: * Repeat steps #5-7
        EXPECTED: 
        """
        pass

    def test_014_add_sportrace_selection_from_inspired_virtual_sports_to_quick_bet_and_repeat_steps_3_10(self):
        """
        DESCRIPTION: Add <Sport>/<Race> selection from Inspired Virtual Sports to Quick Bet and repeat steps #3-10
        EXPECTED: 
        """
        pass

    def test_015_add_sportrace_selection_from_betradar_virtual_tournament_to_quick_bet_and_repeat_steps_3_10(self):
        """
        DESCRIPTION: Add <Sport>/<Race> selection from BetRadar Virtual Tournament to Quick Bet and repeat steps #3-10
        EXPECTED: 
        """
        pass
