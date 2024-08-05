import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869689_To_archive_after_OX100Verify_Forecast__Tricast_Availability(Common):
    """
    TR_ID: C869689
    NAME: [To archive after OX100]Verify 'Forecast' / 'Tricast' Availability
    DESCRIPTION: This test case verifies in what conditions forecast / tricast options will be available on the Bet Slip for
    DESCRIPTION: *   Virtual Motorsports (Class ID 288)
    DESCRIPTION: *   Virtual Cycling (Class ID 290)
    DESCRIPTION: *   Virtual Horse Racing (Class ID 285)
    DESCRIPTION: *   Virtual Greyhound Racing (Class ID 286)
    DESCRIPTION: *   Virtual Grand National (Class ID 26604)
    DESCRIPTION: **JIRA Ticket** :
    DESCRIPTION: BMA-9397 'Extend Forecast and Tricast betting to Virtual Sports'
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_go_to_virtual_sports(self):
        """
        DESCRIPTION: Load Oxygen and go to "Virtual Sports"
        EXPECTED: "Virtual Horse Racing" page is opened by default
        EXPECTED: Next event is shown
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

    def test_004_select_the_latest_buildcomplexlegs_request_in_network_tab_of_the_dev_tools(self):
        """
        DESCRIPTION: Select the latest 'buildComplexLegs' request in "Network" tab of the dev tools
        EXPECTED: The details for 'buildComplexLegs' request is shown
        """
        pass

    def test_005_select_preview_tab_on_the_request_details_and_open_complexleg_record(self):
        """
        DESCRIPTION: Select 'Preview' tab on the request details and open "complexLeg" record
        EXPECTED: if id =FORECAST or id = TRICAST for  ["outcomeCombiRef"] -  the forecast / tricast bets will be available for the event
        """
        pass

    def test_006_verify_forecast__tricast_bets(self):
        """
        DESCRIPTION: Verify 'Forecast' / 'Tricast' bets
        EXPECTED: 'Forecast' / 'Tricast' bets are shown in the 'Singles' section
        """
        pass

    def test_007_add_two_or_three_selections_from_the_same_events_but_from_different_markets(self):
        """
        DESCRIPTION: Add two or three selections from the same events but from different markets
        EXPECTED: Selections are added
        """
        pass

    def test_008_open_bet_slip_and_verify_forecast__tricast_bets(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast' / 'Tricast' bets
        EXPECTED: 'Forecast' / 'Tricast' bets are NOT available if selections from different markets are added
        """
        pass

    def test_009_add_two_or_more_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or more selections from different events to the Bet Slip
        EXPECTED: Selections are added to the Bet Slip
        """
        pass

    def test_010_opne_bet_slip_and_verifty_forecast__tricast_bets(self):
        """
        DESCRIPTION: Opne Bet Slip and verifty 'Forecast' / 'Tricast' bets
        EXPECTED: Forecast' / 'Tricast' bets are NOT available if selections from different events are added
        """
        pass

    def test_011_add_two_or_more_sport_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or more <Sport> selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_012_verify_forecast__tricast_bets(self):
        """
        DESCRIPTION: Verify 'Forecast / Tricast' bets
        EXPECTED: 'Forecast / Tricast' bets are NOT available for <Sport> events
        """
        pass
