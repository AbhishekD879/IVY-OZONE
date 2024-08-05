import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C58836452_Verify_that_Outcome_details_are_taken_from_buildBet_for_Sport_selections_and_actions_in_Betslip(Common):
    """
    TR_ID: C58836452
    NAME: Verify that Outcome details are taken from <buildBet>  for <Sport> selections and actions in Betslip
    DESCRIPTION: Test case verifies data source being set as BPP for certain actions regarding <Sport> selections within Betslip.
    PRECONDITIONS: * Upcoming events should be present for a chosen sport
    PRECONDITIONS: * Surface bet should be configured for the upcoming sport event, containing active selection
    PRECONDITIONS: * Oxygen app should be opened
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * QuickBet should be disabled for mobile responsive mode
    PRECONDITIONS: DevTools should be opened (Click on 'Inspect') -> 'Network' tab -> 'XHR' filter
    PRECONDITIONS: 'Simple' value should be set within Filter for XHR requests list in DevTools
    PRECONDITIONS: **SLP** = Sports Landing Page
    PRECONDITIONS: **EDP** = Event Details Page
    PRECONDITIONS: **NOTE:** EDP 'Simple' SS request is sent once the page is opened; Also 'Simple' SS request is present when SLP is opened - this is a correct behavior.
    """
    keep_browser_open = True

    def test_001_navigate_to_slp_of_any_sport_with_event_cardsand_selections_being_shown_on_the_page(self):
        """
        DESCRIPTION: Navigate to SLP of any 'sport' with event cards(and selections) being shown on the page
        EXPECTED: Page contains event(s)/list(s) with selections
        """
        pass

    def test_002_clear_the_requests_table_in_devtools_via_clear_buttonindexphpattachmentsget114053615(self):
        """
        DESCRIPTION: Clear the requests table in DevTools via 'Clear' button
        DESCRIPTION: ![](index.php?/attachments/get/114053615)
        EXPECTED: Requests table in DevTools becomes empty
        """
        pass

    def test_003_add_2_selections_into_betslip(self):
        """
        DESCRIPTION: Add 2 selections into Betslip
        EXPECTED: * BuildBet requests are sent to BPP
        EXPECTED: * Second request contains bet data regarding the price, status, etc. of both selections
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains added selection is not sent after this action
        EXPECTED: ![](index.php?/attachments/get/114053626) ![](index.php?/attachments/get/114053629)
        """
        pass

    def test_004_tap_on_x_button_in_the_betslip_to_remove_any_selection(self):
        """
        DESCRIPTION: Tap on 'X' button in the Betslip to remove any selection
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of the remaining selection
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains removed selection is not sent after this action
        EXPECTED: ![](index.php?/attachments/get/114053638) ![](index.php?/attachments/get/114053641)
        """
        pass

    def test_005_close_betslip_and_open_edp_of_the_event_that_contains_surface_betindexphpattachmentsget114053649(self):
        """
        DESCRIPTION: Close Betslip and open EDP of the event that contains 'Surface Bet'
        DESCRIPTION: ![](index.php?/attachments/get/114053649)
        EXPECTED: * Event details page is opened
        EXPECTED: * 'Surface Bet' container is shown above the first market
        """
        pass

    def test_006_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 
        """
        pass

    def test_007_add_surface_bet_selection_into_betslip_by_tappingclicking_on_it(self):
        """
        DESCRIPTION: Add Surface Bet selection into BetSlip by tapping/clicking on it
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of both new and previously added selections
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains added selection is not sent after this action
        EXPECTED: ![](index.php?/attachments/get/114053654) ![](index.php?/attachments/get/114053658)
        """
        pass

    def test_008_click_on_selection_within_surface_bet_again(self):
        """
        DESCRIPTION: Click on selection within Surface Bet again
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of the remaining selection
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains removed selection is not sent after this action
        EXPECTED: ![](index.php?/attachments/get/114053662) ![](index.php?/attachments/get/114053660)
        """
        pass
