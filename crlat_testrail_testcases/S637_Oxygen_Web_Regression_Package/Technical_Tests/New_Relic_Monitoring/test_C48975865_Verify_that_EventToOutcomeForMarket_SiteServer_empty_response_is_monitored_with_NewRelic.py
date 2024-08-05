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
class Test_C48975865_Verify_that_EventToOutcomeForMarket_SiteServer_empty_response_is_monitored_with_NewRelic(Common):
    """
    TR_ID: C48975865
    NAME: Verify that EventToOutcomeForMarket SiteServer empty response is monitored with NewRelic
    DESCRIPTION: This test case verifies that NewRelic monitoring counter increased when SiteServer response for EventToOutcomeForMarket was received without market and selection details
    PRECONDITIONS: 1. CMS configuration:
    PRECONDITIONS: System configuration > Structure > SiteServerLiveMarkets
    PRECONDITIONS: -enabled = Yes
    PRECONDITIONS: -sportCategoriesIds field is empty (empty means that its enabled for all categories, otherwise categories should be listed comma separated)
    PRECONDITIONS: -delayMilliseconds = 0 (delay in milliseconds - time between receiving Push update and making request to SiteServer - BMA-50450)
    PRECONDITIONS: 2. Undisplayed market with Displayed selections in TI is present, market should be 'Bet In Running'
    PRECONDITIONS: 3. EDP page is opened in App
    PRECONDITIONS: 4. DevTools (Network tab) is opened in Browser
    PRECONDITIONS: 5. EventToOutcomeForMarket responses examples:
    PRECONDITIONS: "Empty" response (missing 'event' object):
    PRECONDITIONS: ![](index.php?/attachments/get/56623778)
    PRECONDITIONS: NOT "Empty" response ('event' object received):
    PRECONDITIONS: ![](index.php?/attachments/get/56623779)
    """
    keep_browser_open = True

    def test_001__set_market_from_preconditions_to_displayed_in_ti_open_browser_and_observe_devtools_network_tab(self):
        """
        DESCRIPTION: -Set market from preconditions to 'Displayed' in TI
        DESCRIPTION: -Open Browser and observe DevTools Network tab
        EXPECTED: 'push' request has a response with new market and parameter "displayed": "Y"
        """
        pass

    def test_002__check_that_eventtooutcomeformarket_ss_request_is_sent_right_after_push_message_in_devtools_open_eventtooutcomeformarket_response(self):
        """
        DESCRIPTION: -Check that EventToOutcomeForMarket SS request is sent right after Push message
        DESCRIPTION: -In devtools open EventToOutcomeForMarket response
        EXPECTED: New SS request /EventToOutcomeForMarket/ is sent (with delay value set in CMS = 0 seconds)
        EXPECTED: (ex. Request URL: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForMarket/151281481?&translationLang=en&responseFormat=json )
        EXPECTED: Repeat Step 1 util you receive "Empty" EventToOutcomeForMarket response (usually we receive "Empty" response ~3 out of 10 times):
        EXPECTED: ![](index.php?/attachments/get/56623777)
        EXPECTED: Please see Preconditions for NOT "Empty" response to compare.
        """
        pass

    def test_003_open_newrelic_and_check_monitoring_counter__navigate_httpsinsightsnewreliccom__enter_nrql_queryselect__from__pageaction_where_actionname__edplivemarketoutcomesinfoavailable_or_actionname__edplivemarketinfoavailable_since_1_day_ago_limit_max(self):
        """
        DESCRIPTION: Open NewRelic and check monitoring counter
        DESCRIPTION: - Navigate https://insights.newrelic.com/
        DESCRIPTION: - Enter NRQL query:
        DESCRIPTION: SELECT * FROM  PageAction where actionName = 'EDPLiveMarketOutcomesInfoAvailable' OR actionName = 'EDPLiveMarketInfoAvailable' SINCE 1 day ago LIMIT MAX
        EXPECTED: - 'EDPLiveMarketInfoAvailable' = 'false' in case market is NOT available (i.e. "Empty" EventToOutcomeForMarket response is received).
        EXPECTED: And 'true' in case market available.
        EXPECTED: - 'EDPLiveMarketOutcomesInfoAvailable' = 'false' in case selection is NOT available (i.e. EventToOutcomeForMarket response is received with market info but without Outcomes(selections) in it)
        EXPECTED: And 'true' in case selection available
        EXPECTED: ![](index.php?/attachments/get/58811028)
        """
        pass
