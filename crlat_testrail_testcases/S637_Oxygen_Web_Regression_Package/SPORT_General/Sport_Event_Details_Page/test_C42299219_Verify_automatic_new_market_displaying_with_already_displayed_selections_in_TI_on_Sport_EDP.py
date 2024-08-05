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
class Test_C42299219_Verify_automatic_new_market_displaying_with_already_displayed_selections_in_TI_on_Sport_EDP(Common):
    """
    TR_ID: C42299219
    NAME: Verify automatic new market displaying  (with already displayed selections in TI) on <Sport> EDP
    DESCRIPTION: TC verifies that new market is displayed on EDP automatically when market is set to 'Displayed' in TI and it already has 'Displayed' selections.
    DESCRIPTION: (Actual for Ladbrokes >100.3, not released for Coral yet!)
    PRECONDITIONS: 1. CMS configuration:
    PRECONDITIONS: System configuration > Structure > SiteServerLiveMarkets
    PRECONDITIONS: -enabled = Yes
    PRECONDITIONS: -sportCategoriesIds field is empty (empty means that its enabled for all categories, otherwise categories should be listed comma separated)
    PRECONDITIONS: -delayMilliseconds = 2000 (delay in milliseconds - time between receiving Push update and making request to SiteServer - BMA-50450)
    PRECONDITIONS: 2. Undisplayed market with Displayed selections in TI is present, market should be 'Bet In Running'
    PRECONDITIONS: 3. EDP page is opened in App
    PRECONDITIONS: 4. DevTools (Network tab) is opened in Browser
    """
    keep_browser_open = True

    def test_001__set_market_from_preconditions_to_displayed_in_ti_open_browser_and_observe_devtools_network_tab(self):
        """
        DESCRIPTION: -Set market from preconditions to 'Displayed' in TI
        DESCRIPTION: -Open Browser and observe DevTools Network tab
        EXPECTED: 'push' request has a response with new market and parameter "displayed": "Y"
        """
        pass

    def test_002_check_if_ss_request_is_sent_after_push_message(self):
        """
        DESCRIPTION: Check if SS request is sent after Push message
        EXPECTED: New SS request /EventToOutcomeForMarket/ is sent (with delay value set in CMS).
        EXPECTED: Response contains information about market and selections.
        EXPECTED: (ex. Request URL: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForMarket/151281481?&translationLang=en&responseFormat=json )
        """
        pass

    def test_003_check_that_new_market_is_displayed_on_edp(self):
        """
        DESCRIPTION: Check that new market is displayed on EDP
        EXPECTED: Market is displayed on EDP
        """
        pass
