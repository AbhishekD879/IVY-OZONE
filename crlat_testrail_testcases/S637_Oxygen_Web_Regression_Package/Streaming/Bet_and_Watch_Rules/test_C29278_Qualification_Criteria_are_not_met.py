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
class Test_C29278_Qualification_Criteria_are_not_met(Common):
    """
    TR_ID: C29278
    NAME: Qualification Criteria are not met
    DESCRIPTION: This test case verifies that user is not able to watch a stream if Bet and Watch qualification rules are not met for the event
    PRECONDITIONS: 1. SiteServer event should be configured to support streaming provider and should have event mapped (**'typeFlagCodes'** AND corresponding **'drilldownTagNames'** flags should be set)
    PRECONDITIONS: {typeFlagCodes=AVA and drilldownTagNames=EVFLAG_AVA} or
    PRECONDITIONS: {typeFlagCodes=RVA and drilldownTagNames=EVFLAG_RVA} or
    PRECONDITIONS: {typeFlagCodes=RPG and drilldownTagNames=EVFLAG_RPM}
    PRECONDITIONS: 2. Applicable to Horse Racing and Greyhounds only
    PRECONDITIONS: NOTE: contact UAT team for all configurations
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_open_details_page_of_horse_racing_event_which_satisfies_preconditions_and_has_isstarted__true(self):
        """
        DESCRIPTION: Open details page of Horse Racing event which satisfies Preconditions and has **isStarted = true**
        EXPECTED: 'Stream' icon is available for this event
        """
        pass

    def test_003_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: User is NOT able to watch a stream successfully
        EXPECTED: Message is received: "In order to watch this stream, you must be logged in."
        """
        pass

    def test_004_login_to_application_using_credentials_with_positive_balance(self):
        """
        DESCRIPTION: Login to application using credentials with positive balance
        EXPECTED: 
        """
        pass

    def test_005_open_details_page_of_event_which_satisfies_preconditions_and_has_isstartedtrue(self):
        """
        DESCRIPTION: Open details page of event which satisfies Preconditions and has **isStarted=true**
        EXPECTED: 'Video Stream' button is available for this event
        """
        pass

    def test_006_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: User is NOT able to watch a stream successfully
        EXPECTED: Message is displayed: "In order to view this event you should place a bet greater than or equal to £1.00."
        """
        pass

    def test_007_open_details_page_of_horse_racing_event_which_satisfies_preconditions_and_hasisstarted__true(self):
        """
        DESCRIPTION: Open details page of Horse Racing event which satisfies Preconditions and has **isStarted != true**
        EXPECTED: 
        """
        pass

    def test_008_place_a_bet_for_100_stake_on_one_selection_within_tested_event_eg_050p(self):
        """
        DESCRIPTION: Place a bet for < ​£1.00 stake on one selection within tested event (e.g. 0.50p)
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_009_navigate_back_to_the_event_and_wait_until_it_is_started_isstartedtrue(self):
        """
        DESCRIPTION: Navigate back to the event and wait until it is started (isStarted=true)
        EXPECTED: 
        """
        pass

    def test_010_tap_stream_icon(self):
        """
        DESCRIPTION: Tap 'Stream' icon
        EXPECTED: User is NOT able to watch a stream successfully
        EXPECTED: Message is displayed: "In order to view this event you should place a bet greater than or equal to £1.00"
        """
        pass

    def test_011_open_details_page_of_horse_racing_event_which_satisfies_preconditions_and_hasisstarted__true(self):
        """
        DESCRIPTION: Open details page of Horse Racing event which satisfies Preconditions and has **isStarted != true**
        EXPECTED: 
        """
        pass

    def test_012_place_a_bet_for100_stake_on_one_selection_within_tested_event(self):
        """
        DESCRIPTION: Place a bet for £1.00 stake on one selection within tested event
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_013_navigate_back_to_the_event_and_wait_until_it_is_started_isstartedtrue(self):
        """
        DESCRIPTION: Navigate back to the event and wait until it is started (isStarted=true)
        EXPECTED: 
        """
        pass

    def test_014_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: User is able to watch a stream successfully
        """
        pass

    def test_015_open_details_page_of_another_event_which_satisfies_preconditions_and_isstartedtrue_however_bet_was_not_placed_for_it(self):
        """
        DESCRIPTION: Open details page of another event which satisfies Preconditions and isStarted=true, however bet was not placed for it
        EXPECTED: 'Stream' icon is available for this event
        """
        pass

    def test_016_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: User is NOT able to watch a stream successfully
        EXPECTED: Message is displayed: "In order to view this event you should place a bet greater than or equal to £1.00"
        """
        pass

    def test_017_repeat_steps_2_17_for_greyhounds(self):
        """
        DESCRIPTION: Repeat steps 2-17 for Greyhounds
        EXPECTED: 
        """
        pass
