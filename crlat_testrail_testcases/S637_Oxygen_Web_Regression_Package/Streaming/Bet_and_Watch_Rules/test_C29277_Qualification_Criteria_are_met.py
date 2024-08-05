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
class Test_C29277_Qualification_Criteria_are_met(Common):
    """
    TR_ID: C29277
    NAME: Qualification Criteria are met
    DESCRIPTION: This test case verifies that qualification criteria for watching streams for Horse Racing and Greyhound events are applied correctly
    PRECONDITIONS: 1. SiteServer event should be configured to support streaming provider and should have event mapped (**'typeFlagCodes'** AND corresponding **'drilldownTagNames'** flags should be set)
    PRECONDITIONS: {typeFlagCodes=AVA and drilldownTagNames=EVFLAG_AVA} or
    PRECONDITIONS: {typeFlagCodes=RVA and drilldownTagNames=EVFLAG_RVA} or
    PRECONDITIONS: {typeFlagCodes=RPG and drilldownTagNames=EVFLAG_RPM}
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: *   isStarted = "true"
    PRECONDITIONS: 3. Applicable for Horse Racing and Greyhounds only
    PRECONDITIONS: NOTE: contact UAT team for all configurations
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_login_to_application_using_credentials_with_positive_balance(self):
        """
        DESCRIPTION: Login to application using credentials with positive balance
        EXPECTED: 
        """
        pass

    def test_003_open_details_page_of_horse_racing_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open details page of Horse Racing event which satisfies Preconditions
        EXPECTED: 'Video Stream' button is available for this event
        """
        pass

    def test_004_place_a_bet_for_100_stake_on_one_selection_within_tested_event(self):
        """
        DESCRIPTION: Place a bet for £1.00 stake on one selection within tested event
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_005_navigate_back_to_the_event(self):
        """
        DESCRIPTION: Navigate back to the event
        EXPECTED: 
        """
        pass

    def test_006_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: User is able to watch a stream successfully
        """
        pass

    def test_007_open_details_page_of_another_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open details page of another event which satisfies Preconditions
        EXPECTED: 'Stream' icon is available for this event
        """
        pass

    def test_008_place_several_bets_withing_the_same_event_for_sum_of100eg_050p_plus_050p_or_030p_plus_07p_etc(self):
        """
        DESCRIPTION: Place several bets withing the same event for sum of £1.00 (e.g. 0.50p + 0.50p, or 0.30p + 0.7p, etc)
        EXPECTED: 
        """
        pass

    def test_009_navigate_back_to_the_event(self):
        """
        DESCRIPTION: Navigate back to the event
        EXPECTED: 
        """
        pass

    def test_010_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: User is able to watch a stream successfully
        """
        pass

    def test_011_open_details_page_of_another_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open details page of another event which satisfies Preconditions
        EXPECTED: 'Stream' icon is available for this event
        """
        pass

    def test_012_place_a_bet_with_a_stake_100(self):
        """
        DESCRIPTION: Place a bet with a Stake > £1.00
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_013_navigate_back_to_the_event(self):
        """
        DESCRIPTION: Navigate back to the event
        EXPECTED: 
        """
        pass

    def test_014_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: User is able to watch a stream successfully
        """
        pass

    def test_015_open_details_page_of_greyhounds_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open details page of Greyhounds event which satisfies Preconditions
        EXPECTED: 'Video Stream' button is available for this event
        """
        pass

    def test_016_repeat_steps_4_14(self):
        """
        DESCRIPTION: Repeat steps 4-14
        EXPECTED: 
        """
        pass
