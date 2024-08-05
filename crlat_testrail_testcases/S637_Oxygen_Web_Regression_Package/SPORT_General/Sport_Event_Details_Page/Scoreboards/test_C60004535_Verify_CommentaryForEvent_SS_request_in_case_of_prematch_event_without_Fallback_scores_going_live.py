import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C60004535_Verify_CommentaryForEvent_SS_request_in_case_of_prematch_event_without_Fallback_scores_going_live(Common):
    """
    TR_ID: C60004535
    NAME: Verify /CommentaryForEvent SS request in case of prematch event without Fallback scores going live
    DESCRIPTION: This test case verifies prematch event without Fallback scores going live and presence of "CommentaryForEvent" request after navigation to EDP.
    PRECONDITIONS: 1. Find any prematch event from Football or Badminton sports that doesn't have Fallback Scores mapped.
    PRECONDITIONS: 2. Login to Oxygen and navigate to Event Details Page of the Event from Step 1 in preconditions.
    PRECONDITIONS: Example of "CommentaryForEvent" request:
    PRECONDITIONS: https://{openbetDomain}/openbet-ssviewer/Commentary/2.31/CommentaryForEvent/{eventId}?translationLang=en&responseFormat=json&includeUndisplayed=true
    PRECONDITIONS: How to figure out the type of Scoreboards present for Event:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=145626444
    """
    keep_browser_open = True

    def test_001_verify_that_commentaryforevent_request_is_not_made_after_navigation_to_edp(self):
        """
        DESCRIPTION: Verify that "CommentaryForEvent" request is not made after navigation to EDP.
        EXPECTED: * User is navigated to EDP page
        EXPECTED: * "CommentaryForEvent" request is not made after navigation
        """
        pass

    def test_002_trigger_any_price_updates_for_the_event_from_previous_step_and_verify_that_live_updates_are_received_and_displayed_on_ui(self):
        """
        DESCRIPTION: Trigger any price updates for the Event from previous step and verify that live updates are received and displayed on UI.
        EXPECTED: * Price updates are received and correctly visualised on UI.
        """
        pass

    def test_003_move_event_from_step_1_to_in_play(self):
        """
        DESCRIPTION: Move Event from Step 1 to In-Play
        EXPECTED: 
        """
        pass

    def test_004_navigate_to_edp_of_the_event_from_step_1_and_verify_that_commentaryforevent_request_is_not_made_after_navigation_to_edp(self):
        """
        DESCRIPTION: Navigate to EDP of the Event from Step 1 and verify that "CommentaryForEvent" request is not made after navigation to EDP.
        EXPECTED: * User is navigated to EDP page
        EXPECTED: * "CommentaryForEvent" request is not made after navigation
        """
        pass

    def test_005_trigger_any_price_updates_for_the_event_from_previous_step_and_verify_that_live_updates_are_received_and_displayed_on_ui(self):
        """
        DESCRIPTION: Trigger any price updates for the Event from previous step and verify that live updates are received and displayed on UI.
        EXPECTED: * Price updates are received and correctly visualised on UI.
        """
        pass
