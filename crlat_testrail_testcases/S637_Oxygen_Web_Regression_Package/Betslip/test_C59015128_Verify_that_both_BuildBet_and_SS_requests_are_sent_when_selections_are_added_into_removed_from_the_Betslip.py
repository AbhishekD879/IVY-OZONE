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
class Test_C59015128_Verify_that_both_BuildBet_and_SS_requests_are_sent_when_selections_are_added_into_removed_from_the_Betslip(Common):
    """
    TR_ID: C59015128
    NAME: Verify that both BuildBet and SS requests are sent when selections are added into/removed from the Betslip
    DESCRIPTION: Test case verifies presence(usage) of both SS and BPP requests when selection-oriented actions such as selections 'adding into/removing from' Betslip are executed for certain pages(sports/races).
    PRECONDITIONS: * 'Virtual' sport with at least 2 upcoming events should be present
    PRECONDITIONS: * 'Scorecast' market should be present for the upcoming Football event
    PRECONDITIONS: * 'Forecast'/'Tricast' market should be present for the upcoming <Race> event
    PRECONDITIONS: * Upcoming <Sport>/<Race> event with at least 2 active selections should be present
    PRECONDITIONS: * Oxygen app should be opened
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * QuickBet should be disabled for mobile responsive mode
    PRECONDITIONS: DevTools should be opened (Click on 'Inspect') -> 'Network' tab -> 'XHR' filter
    """
    keep_browser_open = True

    def test_001_navigate_to_virtuals_page(self):
        """
        DESCRIPTION: Navigate to 'Virtuals' page
        EXPECTED: Page contains event(s)/list(s) of markets with selections
        """
        pass

    def test_002_add_2_selections_into_betslip(self):
        """
        DESCRIPTION: Add 2 selections into Betslip
        EXPECTED: * BuildBet requests are sent to BPP
        EXPECTED: * Second request contains bet data regarding the price, status, etc. of both selections
        EXPECTED: * SS requests (filtered by 'Simple') with event IDs that contain added selections are also sent
        EXPECTED: ![](index.php?/attachments/get/113549250)
        EXPECTED: ![](index.php?/attachments/get/113549247)
        EXPECTED: ![](index.php?/attachments/get/113549251)
        """
        pass

    def test_003_click_on_x_button_to_remove_any_selection(self):
        """
        DESCRIPTION: Click on 'X' button to remove any selection
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of the remaining selection
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains remaining selection is also sent
        EXPECTED: ![](index.php?/attachments/get/113549253)
        EXPECTED: ![](index.php?/attachments/get/113549252)
        """
        pass

    def test_004_open_edp_of_the_football_event_that_has_a_configured_scorecast_market_with_active_selections(self):
        """
        DESCRIPTION: Open EDP of the Football event that has a configured 'Scorecast' market with active selections
        EXPECTED: * Page contains market dropdowns with selections
        EXPECTED: * 'Scorecast' market dropdown is present under 'ALL MARKETS' tab
        """
        pass

    def test_005_form_a_scorecast_selection_and_tap_on_its_buttonadd_it_to_betslip(self):
        """
        DESCRIPTION: Form a 'Scorecast' selection and tap on its button(add it to Betslip)
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * BuildBet request contains bet data regarding the price, status, etc. of the selections
        EXPECTED: * SS request (filtered by 'Simple') with event ID that contains added selection is also sent
        EXPECTED: ![](index.php?/attachments/get/113549259)
        EXPECTED: ![](index.php?/attachments/get/113549267)
        """
        pass

    def test_006_open_edp_of_the_event_that_has_at_least_2_active_selections(self):
        """
        DESCRIPTION: Open EDP of the event that has at least 2 active selections
        EXPECTED: Page contains market dropdown(s) with selections
        """
        pass

    def test_007_add_1st_active_selection_into_betslip_and_suspend_it_through_ti(self):
        """
        DESCRIPTION: Add 1st active selection into Betslip and suspend it through TI
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of the remaining selection
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains removed selection is NOT sent
        EXPECTED: ![](index.php?/attachments/get/113549279)
        """
        pass

    def test_008_add_2nd_active_selection_into_betslip(self):
        """
        DESCRIPTION: Add 2nd active selection into Betslip
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Second request contains bet data regarding the price, status, etc. of both selections
        EXPECTED: * SS request (filtered by 'SS') with event IDs that contain added selections is also sent
        EXPECTED: ![](index.php?/attachments/get/113549286)
        EXPECTED: ![](index.php?/attachments/get/113549288)
        """
        pass

    def test_009_open_edp_of_the_ltracegt_event_that_has_a_configured_forecasttricast_market_with_active_selections(self):
        """
        DESCRIPTION: Open EDP of the &lt;Race&gt; event that has a configured 'Forecast'/'Tricast' market with active selections
        EXPECTED: * Page contains market tab(s) with selections list(s)
        EXPECTED: * 'Forecast'/'Tricast' market tab is present in the markets lane(tabs lane)
        """
        pass

    def test_010_form_a_forecasttricast_selection_and_tapclick_on_add_to_betslip_button(self):
        """
        DESCRIPTION: Form a 'Forecast'/'Tricast' selection and tap/click on 'Add to Betslip' button
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * BuildBet request contains bet data regarding the price, status, etc. of the selections
        EXPECTED: * SS request (filtered by 'Simple') with event ID that contains added selection is also sent
        EXPECTED: ![](index.php?/attachments/get/113549305)
        EXPECTED: ![](index.php?/attachments/get/113549300)
        """
        pass
