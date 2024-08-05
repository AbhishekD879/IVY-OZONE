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
class Test_C59917803_Error_Messaging__Active_User_attempting_to_access_Stream(Common):
    """
    TR_ID: C59917803
    NAME: [Error Messaging] - Active User attempting to access Stream
    DESCRIPTION: This test case verifies the display of the error message to a logged in active user that tries to launch a stream with Sports Rules and Racing Rules regardless how long before race they trigger this error.
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
    PRECONDITIONS: * Find and navigate to HR/GH (with Sports Rules) events which have streaming available and start time is more than 10 mins (the list is provided in the description)
    PRECONDITIONS: * Find an event with Racing Rules (any GR/HR event which is not listed above in the description)
    PRECONDITIONS: * Create an active user account
    PRECONDITIONS: * The active user is logged in
    PRECONDITIONS: * Open Devtools -> Filter out XHR in Network
    PRECONDITIONS: Please note that for Sports Rules events the streaming is shown once it's available, until then the message "The stream has not yet started. Please try again soon." is displayed.
    PRECONDITIONS: After fixing BMA-56032 in steps 2 and 3 - the buttons of the pop-up are: "OK, THANKS" & "DEPOSIT"
    """
    keep_browser_open = True

    def test_001_navigate_to_the_event_with_sports_rules_from_preconditions_more_than_10_mins_before_start_time(self):
        """
        DESCRIPTION: Navigate to the event with Sports Rules from preconditions (more than 10 mins before start time)
        EXPECTED: The event is displayed
        """
        pass

    def test_002_click_on_the_live_stream_button(self):
        """
        DESCRIPTION: Click on the 'Live Stream' button
        EXPECTED: * "WATCH LIVE" title
        EXPECTED: * The following error message is displayed:"The stream has not yet started. Please try again soon."
        EXPECTED: * Event countdown (if available)
        EXPECTED: * 'OK' button
        EXPECTED: ![](index.php?/attachments/get/119423955) ![](index.php?/attachments/get/119423956)
        """
        pass

    def test_003_navigate_to_the_event_with_racing_rules_from_preconditions_more_than_10_mins_before_start_time(self):
        """
        DESCRIPTION: Navigate to the event with Racing Rules from preconditions (more than 10 mins before start time)
        EXPECTED: The event is displayed
        """
        pass

    def test_004_click_on_the_live_stream_button(self):
        """
        DESCRIPTION: Click on the 'Live Stream' button
        EXPECTED: * "WATCH LIVE" title
        EXPECTED: * The following error message is displayed:"In order to view this event you need to place a bet greater than or equal to £1."
        EXPECTED: * The Optin response contains the failureCode: "4104"
        EXPECTED: * Event countdown (if available)
        EXPECTED: * 'OK' button
        EXPECTED: ![](index.php?/attachments/get/119423997) ![](index.php?/attachments/get/119423998)
        """
        pass
