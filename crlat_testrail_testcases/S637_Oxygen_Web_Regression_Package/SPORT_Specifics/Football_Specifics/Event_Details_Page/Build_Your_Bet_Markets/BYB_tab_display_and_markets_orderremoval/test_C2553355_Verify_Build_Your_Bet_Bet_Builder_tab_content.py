import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.sports
@vtest
class Test_C2553355_Verify_Build_Your_Bet_Bet_Builder_tab_content(Common):
    """
    TR_ID: C2553355
    NAME: Verify 'Build Your Bet'/'Bet Builder' tab content
    DESCRIPTION: Test case verifies navigation to 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab and tab content
    DESCRIPTION: AUTOTEST [C2594263]
    DESCRIPTION: AUTOTEST [C2594392]
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Dev Tools> Network > XHR: Request to Banach for /events/event_id on EDP should return data
    PRECONDITIONS: To check response from Banach with markets:  **markets-grouped** request
    PRECONDITIONS: To check which of markets are added to CMS : cms/api/bma/byb-markets (BYB > BYB markets in CMS)
    PRECONDITIONS: **Event details page of Banach event is loaded**
    """
    keep_browser_open = True

    def test_001_clicktap_on_the_build_your_bet_coral__bet_builder_ladbrokes_tab(self):
        """
        DESCRIPTION: Click/Tap on the 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab
        EXPECTED: - 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is opened and selected
        EXPECTED: - 'New' icon is shown above 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab name
        EXPECTED: - Url path ends with /build-your-bet **Coral** or /bet-builder **Ladbrokes**
        """
        pass

    def test_002_verify_markets_accordions(self):
        """
        DESCRIPTION: Verify markets accordions
        EXPECTED: - 2 markets accordions are expanded by default
        EXPECTED: - Markets which are coming in **markets-grouped** request and are added in CMS are displayed as market accordions
        """
        pass
