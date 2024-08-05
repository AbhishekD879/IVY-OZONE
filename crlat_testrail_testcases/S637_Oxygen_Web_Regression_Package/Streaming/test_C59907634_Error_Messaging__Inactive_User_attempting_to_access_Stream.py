import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C59907634_Error_Messaging__Inactive_User_attempting_to_access_Stream(Common):
    """
    TR_ID: C59907634
    NAME: [Error Messaging] - Inactive User attempting to access Stream
    DESCRIPTION: This test case verifies the display of the error message to a logged in inactive user that tries to launch a stream with Sports Rules and Racing Rules regardless how long before race they trigger this error.
    DESCRIPTION: Sports Rules:
    DESCRIPTION: 1. Customer has placed a £1 bet in the last 24 hours
    DESCRIPTION: 2. Customer has positive balance
    DESCRIPTION: 3. Customer has placed a £1 pool bet in the last 24 hours
    DESCRIPTION: * ATR UK horse racing streams to be set to ‘Sports Rules’ automatically.
    DESCRIPTION: * Perform/SIS UK horse racing streams to be set to ‘Sports Rules’ automatically.
    DESCRIPTION: * No change on Irish racing streams (should remain 'Racing Rules').
    DESCRIPTION: * Other providers should not be affected
    DESCRIPTION: List with event types that require Sports qualification
    DESCRIPTION: The applicable HR event types can be found here.
    DESCRIPTION: Ascot, Doncaster, Sandown, Cheltenham, Newcastle, Haydock, Kempton, Chepstow, Wetherby, Newbury, Aintree, York, Royal Ascot, Goodwood, Ayr, Bangor-on-Dee, Bath, Beverley, Brighton, Carlisle, Cartmel, Catterick, Chester, Epsom, Epsom Downs, Exeter, Fakenham, Ffos Las, Fontwell, Hamilton, Hereford, Hexham, Huntingdon, Kelso, Leicester, Lingfield, Ludlow, Market Rasen, Musselburgh, Arab Racing Newbury, Newmarket, Newton Abbot, Nottingham, Perth, Plumpton, Pontefract, Redcar, Ripon, Salisbury, Sedgefield, Southwell, Stratford, Taunton, Thirsk, Towcester, Uttoxeter, Wolverhampton, Warwick, Wincanton, Windsor, Worcester, Yarmouth
    DESCRIPTION: HR - https://jira.openbet.com/browse/LCRCORE-19070 & https://jira.openbet.com/browse/LCRCORE-19263
    DESCRIPTION: GH - https://jira.openbet.com/browse/LCRCORE-19781
    PRECONDITIONS: * Find and navigate to HR/GH (with Sports Rules) events which have streaming available and start time is more than 10 mins, 10 mins and less than 10 mins (the list is provided in the description)
    PRECONDITIONS: * Find an event with Racing Rules (any GR/HR event which is not listed above in the description)
    PRECONDITIONS: * Create an inactive user account (0 balance and 0 bets within last 24 hours)
    PRECONDITIONS: * The inactive user is logged in
    PRECONDITIONS: * Open Devtools -> Filter out XHR in Network
    PRECONDITIONS: *Please note* that the message  "This stream has not yet started. Please try again soon" will be shown only once the inactive user becomes active
    PRECONDITIONS: After fixing BMA-56032 in steps 2 and 3 - the buttons of the pop-up are: "OK, THANKS" & "DEPOSIT"
    """
    keep_browser_open = True

    def test_001_navigate_to_the_event_with_sports_rules_from_preconditions_for_example_market_rasen_more_than_10_mins_before_start_time(self):
        """
        DESCRIPTION: Navigate to the event with Sports Rules from preconditions (for example, Market Rasen, more than 10 mins before start time)
        EXPECTED: The event is displayed
        """
        pass

    def test_002_click_on_the_live_stream_button(self):
        """
        DESCRIPTION: Click on the 'Live Stream' button
        EXPECTED: * The following error message is displayed: "In order to watch the race you must have a funded account or have placed a bet in the last 24 hours"
        EXPECTED: * The Optin response contains the failureCode: "4105"
        EXPECTED: * Event countdown before the race is off (if available)
        EXPECTED: ![](index.php?/attachments/get/119423027)![](index.php?/attachments/get/119423026)
        """
        pass

    def test_003_repeat_step_2_with__an_event_that_is_starting_in_10_mins__an_event_that_is_starting_sooner_than_10_minsin_2_3_mins__an_event_with_a_stream_that_has_started(self):
        """
        DESCRIPTION: Repeat step 2 with
        DESCRIPTION: - An event that is starting in 10 mins
        DESCRIPTION: - An event that is starting sooner than 10 mins(in 2-3 mins)
        DESCRIPTION: - An event with a stream that has started
        EXPECTED: * The following error message is displayed: "In order to watch the race you must have a funded account or have placed a bet in the last 24 hours"
        EXPECTED: * The Optin response contains the failureCode: "4105"
        EXPECTED: * Event countdown before the race is off (if available)
        EXPECTED: ![](index.php?/attachments/get/119423160)![](index.php?/attachments/get/119423162)
        EXPECTED: ![](index.php?/attachments/get/119423161)![](index.php?/attachments/get/119423159)
        """
        pass

    def test_004_navigate_to_the_event_with_racing_rules_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the event with Racing Rules from preconditions
        EXPECTED: The event is displayed
        """
        pass

    def test_005_click_on_the_live_stream_button(self):
        """
        DESCRIPTION: Click on the 'Live Stream' button
        EXPECTED: * The following error message is displayed:"In order to view this event you need to place a bet greater than or equal to £1"
        EXPECTED: * The Optin response contains the failureCode: "4104"
        EXPECTED: * Event countdown before the race is off (if available)
        EXPECTED: ![](index.php?/attachments/get/119423359)![](index.php?/attachments/get/119423358)
        """
        pass
