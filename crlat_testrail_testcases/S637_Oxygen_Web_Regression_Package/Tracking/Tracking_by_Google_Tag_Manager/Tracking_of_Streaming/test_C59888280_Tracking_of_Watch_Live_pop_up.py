import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.streaming
@vtest
class Test_C59888280_Tracking_of_Watch_Live_pop_up(Common):
    """
    TR_ID: C59888280
    NAME: Tracking of 'Watch Live' pop-up
    DESCRIPTION: This test case verifies tracking of 'Watch Live' pop-up
    PRECONDITIONS: * Load app
    PRECONDITIONS: * Log in with inactive user (has 0 balance and no bets placed)
    PRECONDITIONS: * Go to Horse Racing/Greyhouds EDP with live stream availble (stream provider may be: ATR, Perform, iGameMedia)
    PRECONDITIONS: * Open Dev Tools -> Console
    """
    keep_browser_open = True

    def test_001_tap_live_stream_button(self):
        """
        DESCRIPTION: Tap 'Live Stream' button
        EXPECTED: 'Watch Live' pop-up is displayed with the next element:
        EXPECTED: * 'In order to watch the race you must be an active user and have placed a bet in the last 24h.'
        EXPECTED: * Race countdown timer
        EXPECTED: * 'Ok, Thanks' and 'Deposit' buttons
        """
        pass

    def test_002_tap_ok_thanks_button(self):
        """
        DESCRIPTION: Tap 'Ok, thanks' button
        EXPECTED: 'Watch Live' pop-up is closed
        """
        pass

    def test_003_type_datalayer_in_console(self):
        """
        DESCRIPTION: Type 'dataLayer' in console
        EXPECTED: The next push is sent to GA:
        EXPECTED: {
        EXPECTED: ‘event’ : ‘trackEvent’,
        EXPECTED: ‘eventCategory’ : ‘streaming’,
        EXPECTED: ‘eventAction’ : ‘pop up',
        EXPECTED: 'eventLabel’: ‘Ok, Thanks’,
        EXPECTED: ‘sportID‘: event.categoryId,
        EXPECTED: ‘typeID‘: event.typeId,
        EXPECTED: ‘eventID‘: event.id
        EXPECTED: }
        EXPECTED: where,
        EXPECTED: sportID - valid OB caregoryID,
        EXPECTED: typeID - valid OB typeID,
        EXPECTED: eventID - valid eventID
        """
        pass

    def test_004_tap_live_stream_button(self):
        """
        DESCRIPTION: Tap 'Live Stream' button
        EXPECTED: 'Watch Live' pop-up is displayed
        """
        pass

    def test_005_tap_anywhere_but_not_watch_live_pop_up(self):
        """
        DESCRIPTION: Tap anywhere but not 'Watch Live' pop-up
        EXPECTED: 'Watch Live' pop-up is closed
        """
        pass

    def test_006_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: 
        """
        pass

    def test_007_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: User is navigated to 'Deposit' page
        """
        pass

    def test_008_type_datalayer_in_console(self):
        """
        DESCRIPTION: Type 'dataLayer' in console
        EXPECTED: The next push is sent to GA:
        EXPECTED: {
        EXPECTED: ‘event’ : ‘trackEvent’,
        EXPECTED: ‘eventCategory’ : ‘streaming’,
        EXPECTED: ‘eventAction’ : ‘pop up',
        EXPECTED: 'eventLabel’: ‘Deposit’,
        EXPECTED: ‘sportID‘: event.categoryId,
        EXPECTED: ‘typeID‘: event.typeId,
        EXPECTED: ‘eventID‘: event.id
        EXPECTED: }
        EXPECTED: where,
        EXPECTED: sportID - valid OB caregoryID,
        EXPECTED: typeID - valid OB typeID,
        EXPECTED: eventID - valid eventID
        """
        pass
