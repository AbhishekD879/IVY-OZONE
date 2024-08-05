import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C2512947_To_archive_in_scope_of_OX_98_Verify_forecasts_tricasts_data_in_the_Network_response(Common):
    """
    TR_ID: C2512947
    NAME: [To archive in scope of OX 98] Verify forecasts/tricasts data in the Network response
    DESCRIPTION: This test case verifies receiving  forecast/tricast data in response
    PRECONDITIONS: 1. User is logged in
    """
    keep_browser_open = True

    def test_001_go_to_the_race_event_details_page(self):
        """
        DESCRIPTION: Go to the <Race> event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_002_add_two_or_more_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or more selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_003_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_004_open_dev_console_via_f12_key(self):
        """
        DESCRIPTION: Open dev console via  F12 key
        EXPECTED: Developer Tools are opened
        """
        pass

    def test_005_select_network_option___tap_xhr_filter_button(self):
        """
        DESCRIPTION: Select 'Network' option -> tap XHR filter button
        EXPECTED: * XHR tab is selected
        EXPECTED: * A list of resources requests is shown
        """
        pass

    def test_006_select_the_latest_buildcomplexlegs_request(self):
        """
        DESCRIPTION: Select the latest 'buildComplexLegs' request
        EXPECTED: The details for 'buildComplexLegs' request is shown
        """
        pass

    def test_007_select_preview_tab_on_the_request_details_and_open_complexleg_record(self):
        """
        DESCRIPTION: Select 'Preview' tab on the request details and open "complexLeg" record
        EXPECTED: id =FORECAST or id = TRICAST is present for  ["outcomeCombiRef"] -  the forecast / tricast bets will be available for the event
        """
        pass

    def test_008_add_two_or_three_selections_from_the_same_event_but_each_from_different_market(self):
        """
        DESCRIPTION: Add two or three selections from the same event but each from different market
        EXPECTED: Selections are added
        """
        pass

    def test_009_open_bet_slip_and_verify_forecasttricast_data_in_response(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast'/'Tricast' data in response
        EXPECTED: There are no data in 'buildComplexLegs' response
        """
        pass

    def test_010_clear_the_betslip_and_add_two_or_more_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Clear the Betslip and add two or more selections from different events to the Bet Slip
        EXPECTED: Selections are added to the Bet Slip
        """
        pass

    def test_011_open_bet_slip_and_verify_forecasttricast_data_in_response(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast'/'Tricast' data in response
        EXPECTED: There are no data in 'buildComplexLegs' response
        """
        pass

    def test_012_clear_the_betslip_and_add_two_or_more_sport_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Clear the Betslip and add two or more <Sport> selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_013_open_bet_slip_and_verify_forecasttricast_data_in_response(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast'/'Tricast' data in response
        EXPECTED: 'buildComplexLegs' respoponse is not received
        """
        pass
