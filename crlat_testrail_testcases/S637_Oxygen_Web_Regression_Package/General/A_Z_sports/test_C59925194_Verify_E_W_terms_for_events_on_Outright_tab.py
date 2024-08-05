import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59925194_Verify_E_W_terms_for_events_on_Outright_tab(Common):
    """
    TR_ID: C59925194
    NAME: Verify E/W terms for events on Outright tab
    DESCRIPTION: This test case verifies E/W terms data on Outright tab
    PRECONDITIONS: 1) At least 1 available 'Outright' should be created and active for the chosen sport category
    PRECONDITIONS: 2) Load Oxygen app
    PRECONDITIONS: 3) Navigate to a chosen Sports Landing Page
    PRECONDITIONS: 4) Switch to 'Outrights' tab
    """
    keep_browser_open = True

    def test_001__expand_any_event_available_sport_type_accordion_pick_available_outright_event(self):
        """
        DESCRIPTION: * Expand any event available sport type accordion
        DESCRIPTION: * Pick available 'Outright' event
        EXPECTED: * Outright page is opened
        EXPECTED: * First two markets are expanded. Other markets accordions are collapsed if present
        """
        pass

    def test_002_check_ew_terms_for_any_available_market(self):
        """
        DESCRIPTION: Check E/W terms for any available market
        EXPECTED: * If market has isEachWayAvailable: "true" parameter, E/W terms are displayed
        EXPECTED: * If market has no 'isEachWayAvailable' parameter at all, E/W terms are NOT displayed
        EXPECTED: ![](index.php?/attachments/get/119596481)
        EXPECTED: ![](index.php?/attachments/get/119596480)
        """
        pass

    def test_003_for_mobile_add_any_selection_from_outrights_page_to_quickbet(self):
        """
        DESCRIPTION: **[For mobile]** Add any selection from 'Outrights' page to QuickBet
        EXPECTED: * If market has isEachWayAvailable: "true" parameter, E/W checkbox is present for market with chosen selection
        EXPECTED: * User could tick E/W checkbox and place a bet
        EXPECTED: * If market of the selection has no 'isEachWayAvailable' parameter at all, E/W checkbox is NOT present
        """
        pass

    def test_004_add_any_selection_from_outrights_page_to_betslip(self):
        """
        DESCRIPTION: Add any selection from 'Outrights' page to Betslip
        EXPECTED: * If market has isEachWayAvailable: "true" parameter, E/W checkbox is present for market with chosen selection
        EXPECTED: * User could tick E/W checkbox and place a bet
        EXPECTED: * If market of the selection has no 'isEachWayAvailable' parameter at all, E/W checkbox is NOT present
        """
        pass
