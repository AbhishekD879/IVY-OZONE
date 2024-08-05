import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C59489077_Verify_loading_of_EDP_with_configured_BYB_when_Banach_does_not_return_data(Common):
    """
    TR_ID: C59489077
    NAME: Verify loading of EDP with configured BYB, when Banach does not return data
    DESCRIPTION: This Test Case verifies that, EDP with configured BYB is loaded, when Banach does not return any data
    PRECONDITIONS: 1. 'Build Your Bet' tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: 2. Banach leagues are added and enabled in CMS -> Your Call -> YourCall Leagues
    PRECONDITIONS: 3. Event belonging to Banach league is mapped (on the Banach side) and created in OpenBet (T.I)
    PRECONDITIONS: 4. BYB markets are added in CMS -> BYB -> BYB Markets
    PRECONDITIONS: 5. 'buildyourbet leagues' response from Banach returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Dev Tools> Network > XHR: Request to Banach for /events/event_id on EDP should return data
    PRECONDITIONS: To check response from Banach with markets: markets-grouped request
    PRECONDITIONS: To check which of markets are added to CMS : cms/api/bma/byb-markets (BYB > BYB markets in CMS)
    PRECONDITIONS: 1. Oxygen application is loaded
    """
    keep_browser_open = True

    def test_001_navigate_to_football_edp_page_of_event_with_configured_banach_markets(self):
        """
        DESCRIPTION: Navigate to Football EDP page of event, with configured Banach Markets
        EXPECTED: 'Build Your Bet' Coral / 'Bet Builder' Ladbrokes tab is present within markets tab
        EXPECTED: Position of 'Build Your Bet' Coral / 'Bet Builder' Ladbrokes tab is defined by EDP-Markets response from CMS
        """
        pass

    def test_002_trigger_banach_service_being_down_block_all_requests_reload_page(self):
        """
        DESCRIPTION: Trigger Banach service being down block all requests. Reload Page
        EXPECTED: Football EDP should be loaded when Banach is down
        EXPECTED: ![](index.php?/attachments/get/115504887)
        """
        pass
