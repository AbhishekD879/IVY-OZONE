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
class Test_C8146657_Desktop_Tracking_of_Successful_Bet_Placement_via_Betslip(Common):
    """
    TR_ID: C8146657
    NAME: Desktop. Tracking of Successful Bet Placement via Betslip
    DESCRIPTION: This test case verify tracking of successful bet placement on Desktop
    PRECONDITIONS: * App is loaded
    PRECONDITIONS: * Quick Bet functionality is disabled in CMS or user`s settings
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop
    """
    keep_browser_open = True

    def test_001_add_a_selections_to_betslip_from_home_screen(self):
        """
        DESCRIPTION: Add a selections to Betslip from Home screen
        EXPECTED: Selection(s) is added
        """
        pass

    def test_002_enter_the_stake_and_place_a_bettype_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Enter the stake and place a bet
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: Data Layer contains action with the following parameters
        EXPECTED: betID: [ids_of_bets]
        EXPECTED: customerBuilt: "No"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "place bet"
        EXPECTED: eventCategory: "betslip"
        EXPECTED: eventLabel: "success"
        EXPECTED: gtm.uniqueEventId: id
        EXPECTED: location: "/"
        """
        pass

    def test_003_navigate_to_different_location_for_ex_footballmatchestodayadd_selections_and_place_bettype_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Navigate to different location, for ex football/matches/today
        DESCRIPTION: Add selections and place bet
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: Data Layer contains action with the following parameters
        EXPECTED: betID: [bet_id]
        EXPECTED: customerBuilt: "No"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "place bet"
        EXPECTED: eventCategory: "betslip"
        EXPECTED: eventLabel: "success"
        EXPECTED: gtm.uniqueEventId:id
        EXPECTED: location: "/sport/football/matches/today"
        """
        pass
