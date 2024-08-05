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
class Test_C59013475_Verify_that_Outcome_details_are_taken_from_buildBet_for_Race_selections_bet_creation_in_Betslip(Common):
    """
    TR_ID: C59013475
    NAME: Verify that Outcome details are taken from <buildBet> for <Race> selections bet creation in Betslip
    DESCRIPTION: Test case verifies data source being set as BPP for certain actions regarding  selections within Betslip.
    PRECONDITIONS: * Upcoming events should be present for a chosen Race type
    PRECONDITIONS: * Selections that have both 'SP' and 'LP' values should be available within the chosen 'Race' event
    PRECONDITIONS: * 'Next Races' module should be configured, containing active selections for upcoming events
    PRECONDITIONS: * Oxygen app should be opened
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * QuickBet should be disabled for mobile responsive mode
    PRECONDITIONS: DevTools should be opened (Click on 'Inspect') -> 'Network' tab -> 'XHR' filter
    PRECONDITIONS: 'Simple' value should be set within Filter for XHR requests list in DevTools
    PRECONDITIONS: SLP = Sports Landing Page
    PRECONDITIONS: EDP = Event Details Page
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racinggreyhounds_slphorse_racingfeaturedgreyhound_racingtoday(self):
        """
        DESCRIPTION: Navigate to Horse Racing/Greyhounds SLP
        DESCRIPTION: '/horse-racing/featured'
        DESCRIPTION: '/greyhound-racing/today'
        EXPECTED: Page contains 'Next Races' module with selections
        """
        pass

    def test_002_add_2_selections_into_betslip(self):
        """
        DESCRIPTION: Add 2 selections into Betslip
        EXPECTED: * BuildBet requests are sent to BPP
        EXPECTED: * Second request contains bet data regarding the price, status, etc. of both selections
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains added selection is not sent
        EXPECTED: ![](index.php?/attachments/get/113549377)
        EXPECTED: ![](index.php?/attachments/get/113549378)
        """
        pass

    def test_003_tap_on_the_x_button_in_the_betslip_to_remove_the_selection(self):
        """
        DESCRIPTION: Tap on the 'X' button in the Betslip to remove the selection
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of the remaining selection
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains removed selection is not sent
        EXPECTED: ![](index.php?/attachments/get/113549379)
        EXPECTED: ![](index.php?/attachments/get/113549381)
        """
        pass

    def test_004__close_betslip_open_edp_of_the_event_that_contains_selections_that_have_both_sp_and_lp_values(self):
        """
        DESCRIPTION: * Close Betslip
        DESCRIPTION: * Open EDP of the event that contains selections that have both 'SP' and 'LP' values
        EXPECTED: Event details page is opened
        """
        pass

    def test_005_add_selection_that_has_both_sp_and_lp_values_into_betslip_by_tapping_on_it(self):
        """
        DESCRIPTION: Add selection that has both 'SP' and 'LP' values into BetSlip by tapping on it
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of both new and previously added selections
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains added selection is not sent
        EXPECTED: ![](index.php?/attachments/get/112736528)
        EXPECTED: ![](index.php?/attachments/get/112736525)
        """
        pass

    def test_006__open_betslip_change_selection_type_from_live_price_value_to_sp_within_the_dropdown_of_stake_cell_for_the_step_5_selection(self):
        """
        DESCRIPTION: * Open Betslip
        DESCRIPTION: * Change selection type from Live Price '#value' to 'SP' within the dropdown of stake cell for the step #5 selection
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of both new and previously added selections
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains added selection is not sent
        EXPECTED: ![](index.php?/attachments/get/112736527)
        EXPECTED: ![](index.php?/attachments/get/112736524)
        """
        pass
